from typing import Union

import click
import os
import json
from dataclasses import asdict

from cod8a.generators.mermaid.class_diagram import convert_json_to_mermaid_class
from cod8a.generators.mermaid.flowchart_diagram import convert_json_to_mermaid_flowchart
from cod8a.generators.mermaid.sequence_diagram import convert_json_to_mermaid_sequence
from enums.diagram_type import DiagramType
from models.models import FileStructure, ProjectStructure
from .parsers.python_parser import PythonParser
from .parsers.dotnet_parser import DotnetParser

# Path to the C# analyzer project
DOTNET_ANALYZER_PATH = os.path.join(os.path.dirname(__file__), "dotnet", "CodeAnalysis", "CodeAnalyzer.csproj")

def get_parser(path: str):
    print(f"Checking analyzer ...")
    isDotnetParser = any(path.endswith(ext) for ext in [".cs", ".csproj", ".sln"]) or os.path.isdir(path) and any(f.endswith(".cs") for _, _, files in os.walk(path) for f in files) 
    if isDotnetParser:
        return DotnetParser(DOTNET_ANALYZER_PATH)
    return PythonParser()

@click.group()
def cli():
    """cod8a - Code analysis and visualization tool."""
    pass

# Generation of UML Diagrams
@cli.command()
@click.option('-p', '--path', help='Specific path of file(s) to analyze')
@click.option('-t', '--type', 'diagram_type', default='class', type=click.Choice([DiagramType.CLASS.value, DiagramType.SEQUENCE.value, DiagramType.FLOWCHART.value]), help='Type of diagram to generate')
@click.option('--json', 'output_json', is_flag=True, help='Output in JSON format')
@click.option('-o', '--output', help='Output file path (saves as .mmd)')
def uml(path, diagram_type, output_json, output):
    """Generate UML diagram (Mermaid format)."""
    target = path or os.getcwd()
    struct = _extract_structure(target)

    if diagram_type == DiagramType.FLOWCHART.value:
        diagram = convert_json_to_mermaid_flowchart(struct)
    elif diagram_type == DiagramType.SEQUENCE.value:
        diagram = convert_json_to_mermaid_sequence(struct)
    else:
        diagram = convert_json_to_mermaid_class(struct)
        
    print(diagram)

# TODO Generating code documentation 
@click.command()
@click.option('-p', '--path', help='Specific path of file(s) to analyze')
@click.option('--json', 'output_json', is_flag=True, help='Output in JSON format')
def doc_cli(path, output_json):
    """Generate documentation (Markdown format)."""
    target = path or os.getcwd()
    struct = _extract_structure(target)


def _extract_structure(path) -> Union[FileStructure | ProjectStructure]:

    target = path or os.getcwd()
    parser = get_parser(target)
    
    pathExists = os.path.exists(path)
    if not pathExists:
        print("Not found")
        return
    
    struct = parser.parse(path or os.getcwd())
    
    return struct

# Main entry point for cod8a
def main():
    cli.add_command(doc_cli, name="doc")
    cli()

# Separate entry point for code8a
def doc_main():
    doc_cli()

if __name__ == "__main__":
    main()
