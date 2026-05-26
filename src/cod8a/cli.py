import click
import os
from dataclasses import asdict

from cod8a.generators.mermaid.class_diagram import convert_json_to_mermaid_class
from cod8a.generators.mermaid.flowchart_diagram import convert_json_to_mermaid_flowchart
from cod8a.generators.mermaid.sequence_diagram import convert_json_to_mermaid_sequence
from cod8a.helpers.cli_helper import extract_structure, save_diagram
from enums.diagram_type import DiagramType


@click.group()
def cli():
    """cod8a - Code analysis and visualization tool."""
    pass

# Generation of UML Diagrams
@cli.command()
@click.option('-p', '--path', help='Specific path of file(s) to analyze')
@click.option('-d', '--diagram', 'diagram_type', default='class', 
              type=click.Choice(["seq", "s", "sequence", "flow", "f", "flowchart", "c", "class"]), 
              help='Type of diagram to generate')
@click.option('--json', 'output_json', is_flag=True, help='Output in JSON format')
@click.option('-o', '--output', help='Output file path (saves as .mmd)')
def uml(path, diagram_type, output_json, output):
    """Generate UML diagram (Mermaid format)."""
    struct = extract_structure(path)
    

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
    save_diagram(struct, canon_type, diagram, output, path)


# TODO Generating code documentation 
@click.command()
@click.option('-p', '--path', help='Specific path of file(s) to analyze')
@click.option('--json', 'output_json', is_flag=True, help='Output in JSON format')
def doc_cli(path, output_json):
    """Generate documentation (Markdown format)."""
    target = path or os.getcwd()
    struct = extract_structure(target)


# Main entry point for cod8a
def main():
    cli.add_command(doc_cli, name="doc")
    cli()

# Separate entry point for code8a
def doc_main():
    doc_cli()

if __name__ == "__main__":
    main()
