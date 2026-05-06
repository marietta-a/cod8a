import click
import os
import json
from dataclasses import asdict
from .parsers.python_parser import PythonParser
from .parsers.dotnet_parser import DotnetParser
from .generators.uml_generator import UMLGenerator
from .generators.doc_generator import DocGenerator

# Path to the C# analyzer project
DOTNET_ANALYZER_PATH = r"E:\Projects\DotNet\Practice\Csharp15\CodeAnalysis\CodeAnalyzer.csproj"

def get_parser(path: str):
    if any(path.endswith(ext) for ext in [".cs", ".csproj", ".sln"]) or os.path.isdir(path) and any(f.endswith(".cs") for _, _, files in os.walk(path) for f in files):
        return DotnetParser(DOTNET_ANALYZER_PATH)
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
    json_data = json.dumps(asdict(struct), indent=2)

    # For uml, this data will be sent to the UML.md for analysis and generation of the mermaid diagram
    with open("UML.md", "w", encoding="utf-8") as f:
        f.write("# UML Analysis\n\n")
        f.write("## Data Structure (JSON)\n")
        f.write("```json\n")
        f.write(json_data)
        f.write("\n```\n\n")
        f.write("## Mermaid Diagram\n")
        f.write("```mermaid\n")
        f.write(mermaid_diagram)
        f.write("\n```\n")

    if output_json:
        print(json_data)
    else:
        print(mermaid_diagram)

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
