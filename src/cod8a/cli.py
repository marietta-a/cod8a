from ast import List
from typing import Union

import click
import os
import json
import re
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
@click.option('-t', '--type', 'diagram_type', default='class', 
              type=click.Choice(["seq", "s", "sequence", "flow", "f", "flowchart", "c", "class"]), 
              help='Type of diagram to generate')
@click.option('--json', 'output_json', is_flag=True, help='Output in JSON format')
@click.option('-o', '--output', help='Output file path (saves as .mmd)')
def uml(path, diagram_type, output_json, output):
    """Generate UML diagram (Mermaid format)."""
    target = path or os.getcwd()
    struct = _extract_structure(target)

    if not struct:
        click.echo("Error: Could not extract structure.")
        return

    canon_type = "class"
    if DiagramType.FLOWCHART.value.startswith(diagram_type):
        diagram = convert_json_to_mermaid_flowchart(struct)
        canon_type = "flowchart"
    elif DiagramType.SEQUENCE.value.startswith(diagram_type):
        diagram = convert_json_to_mermaid_sequence(struct)
        canon_type = "sequence"
    else:
        diagram = convert_json_to_mermaid_class(struct)
        canon_type = "class"
        
    print(diagram)
    
    # Save diagram
    _save_diagram(struct, canon_type, diagram, output, path)

def _save_diagram(struct, canon_type, content, output=None, path=None):
    """Helper to save mermaid diagram."""
    try:
        file_path = None
        
        # Prepare filename (PascalCase)
        raw_name = getattr(struct, "name", "diagram")
        base_name = os.path.splitext(raw_name)[0]
        # Split by non-alphanumeric and capitalize first letter of each part, preserving internal caps
        pascal_name = "".join(word[0].upper() + word[1:] for word in re.split(r'[^a-zA-Z0-9]', base_name) if word)
        
        if not pascal_name:
            pascal_name = "GeneratedDiagram"
            
        # Append diagram type suffix
        suffix_map = {"class": "Class", "flowchart": "Flowchart", "sequence": "Sequence"}
        pascal_name += suffix_map.get(canon_type, "")

        if output:
            # If output is a directory, use it as base
            if os.path.isdir(output):
                file_path = os.path.join(output, f"{pascal_name}.mmd")
            else:
                # If output is a file path, use it, ensuring .mmd extension
                file_path = output
                if not file_path.endswith(".mmd"):
                    file_path += ".mmd"
        else:
            # If no output provided, prompt the user
            if click.confirm("\nDo you want to save the diagram to a file?", default=True):
                # Save in docs/mermaid at project root
                project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
                save_dir = os.path.join(project_root, "docs", "mermaid")
                file_path = os.path.join(save_dir, f"{pascal_name}.mmd")
        
        if file_path:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
            with open(file_path, "w") as f:
                f.write(content)
            click.echo(f"Diagram exported to: {file_path}")
            
    except Exception as e:
        click.echo(f"Warning: Could not export diagram: {e}")

# TODO Generating code documentation 
@click.command()
@click.option('-p', '--path', help='Specific path of file(s) to analyze')
@click.option('--json', 'output_json', is_flag=True, help='Output in JSON format')
def doc_cli(path, output_json):
    """Generate documentation (Markdown format)."""
    target = path or os.getcwd()
    struct = _extract_structure(target)


def _extract_structure(path) -> Union[FileStructure | ProjectStructure | List[FileStructure]]:

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
