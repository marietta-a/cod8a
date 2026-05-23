import click
import os
import json
from dataclasses import asdict

from cod8a.generators.mermaid.class_diagram import convert_json_to_mermaid
from .parsers.python_parser import PythonParser
from .parsers.dotnet_parser import DotnetParser
from .generators.uml_generator import UMLGenerator
from .generators.doc_generator import DocGenerator

# Path to the C# analyzer project
DOTNET_ANALYZER_PATH = os.path.join(os.path.dirname(__file__), "dotnet", "CodeAnalysis", "CodeAnalyzer.csproj")

def get_parser(path: str):
    print(f"Checking path: {DOTNET_ANALYZER_PATH}")
    if any(path.endswith(ext) for ext in [".cs", ".csproj", ".sln"]) or os.path.isdir(path) and any(f.endswith(".cs") for _, _, files in os.walk(path) for f in files):
        return DotnetParser(DOTNET_ANALYZER_PATH, path)
    return PythonParser()

@click.group()
def cli():
    """cod8a - Code analysis and visualization tool."""
    pass

@cli.command()
@click.option('-f', '--file', help='Specific file to analyze')
@click.option('-p', '--project', help='Project directory to analyze')
@click.option('--json', 'output_json', is_flag=True, help='Output in JSON format')
@click.option('-t', '--type', 'diagram_type', default='class', type=click.Choice(['class', 'flowchart', 'sequence']), help='Type of diagram to generate')
@click.option('-o', '--output', help='Output file path (saves as .mmd)')
def uml(file, project, output_json, diagram_type, output):
    """Generate UML diagram (Mermaid format)."""
    target = file or project or os.getcwd()
    parser = get_parser(target)
    
    if file:
        if isinstance(parser, PythonParser):
            struct = parser.parse_file(file)
        else:
            struct = parser.parse()
    else:
        if isinstance(parser, PythonParser):
            from ..models.models import ProjectStructure
            files = parser.parse_project(project or os.getcwd())
            struct = ProjectStructure(name=os.path.basename(project or os.getcwd()), files=files)
        else:
            struct = parser.parse()

    # if output_json:
    #     if hasattr(struct, 'model_dump'):
    #         print(json.dumps(struct.model_dump(), indent=2))
    #     else:
    #         print(json.dumps(asdict(struct), indent=2))
    #     return

    # generator = UMLGenerator()
    # mermaid_diagram = generator.generate(struct, diagram_type=diagram_type)
    convert_json_to_mermaid(struct)

    # if output:
    #     # Ensure directory exists
    #     out_dir = os.path.dirname(output)
    #     if out_dir:
    #         os.makedirs(out_dir, exist_ok=True)
    #     with open(output, "w", encoding="utf-8") as f:
    #         f.write(mermaid_diagram)
    #     print(f"Diagram saved to {output}")
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
            from ..models.models import ProjectStructure
            files = parser.parse_project(project or os.getcwd())
            struct = ProjectStructure(name=os.path.basename(project or os.getcwd()), files=files)
        else:
            struct = parser.parse(project or os.getcwd())

    convert_json_to_mermaid(struct)
    
    return struct

    # if output_json:
    #     print(json.dumps(asdict(struct), indent=2))
    # else:
    #     generator = DocGenerator()
    #     print(generator.generate(struct))

# Main entry point for cod8a
def main():
    cli.add_command(doc_cli, name="doc")
    cli()

# Separate entry point for cde8a
def doc_main():
    doc_cli()

if __name__ == "__main__":
    main()
