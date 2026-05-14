import click
import os
import json
from dataclasses import asdict
from .parsers.python_parser import PythonParser
from .parsers.dotnet_parser import DotnetParser
from .generators.uml_generator import UMLGenerator
from .generators.doc_generator import DocGenerator

# Path to the C# analyzer project
## On Mac
DOTNET_ANALYZER_PATH = "dotnet/CodeAnalysis/CodeAnalyzer.csproj"
## On Windows
# DOTNET_ANALYZER_PATH = "dotnet\CodeAnalysis\CodeAnalyzer.csproj"

def get_parser(path: str):
    dirname = os.path.dirname(__file__)
    project_root = os.path.join(dirname, DOTNET_ANALYZER_PATH)
    print(f"Checking path: {project_root}")
    if any(path.endswith(ext) for ext in [".cs", ".csproj", ".sln"]) or os.path.isdir(path) and any(f.endswith(".cs") for _, _, files in os.walk(path) for f in files):
        return DotnetParser(project_root)
    return PythonParser()

@click.group()
def cli():
    """cod8a - Code analysis and visualization tool."""
    pass

@cli.command()
@click.option('-f', '--file', help='Specific file to analyze')
@click.option('-p', '--project', help='Project directory to analyze')
@click.option('--json', 'output_json', is_flag=True, help='Output in JSON format')
def uml(file, project, output_json):
    """Generate UML diagram (Mermaid format)."""
    target = file or project or os.getcwd()
    parser = get_parser(target)
    
    if file:
        if isinstance(parser, PythonParser):
            struct = parser.parse_file(file)
        else:
            struct = parser.parse(os.path.dirname(file), os.path.basename(file))
    else:
        if isinstance(parser, PythonParser):
            from .models import ProjectStructure
            files = parser.parse_project(project or os.getcwd())
            struct = ProjectStructure(name=os.path.basename(project or os.getcwd()), files=files)
        else:
            struct = parser.parse(project or os.getcwd())

    generator = UMLGenerator()
    mermaid_diagram = generator.generate(struct)
    # json_data = json.dumps(asdict(struct), indent=2)

    print(mermaid_diagram)
    # if output_json:
    #     print(json_data)
    # else:
    #     print(mermaid_diagram)

@click.command()
@click.option('-f', '--file', help='Specific file to document')
@click.option('-p', '--project', help='Project directory to document')
@click.option('--json', 'output_json', is_flag=True, help='Output in JSON format')
def doc_cli(file, project, output_json):
    """Generate documentation (Markdown format)."""
    target = file or project or os.getcwd()
    parser = get_parser(target)
    
    if file:
        if isinstance(parser, PythonParser):
            struct = parser.parse_file(file)
        else:
            struct = parser.parse(os.path.dirname(file), os.path.basename(file))
    else:
        if isinstance(parser, PythonParser):
            from .models import ProjectStructure
            files = parser.parse_project(project or os.getcwd())
            struct = ProjectStructure(name=os.path.basename(project or os.getcwd()), files=files)
        else:
            struct = parser.parse(project or os.getcwd())

    if output_json:
        print(json.dumps(asdict(struct), indent=2))
    else:
        generator = DocGenerator()
        print(generator.generate(struct))

# Main entry point for cod8a
def main():
    cli.add_command(doc_cli, name="doc")
    cli()

# Separate entry point for cde8a
def doc_main():
    doc_cli()

if __name__ == "__main__":
    main()
