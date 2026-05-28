import click
import os
from dataclasses import asdict

from cod8a.generators.mermaid.class_diagram import generate_class_diagram
from cod8a.generators.mermaid.flowchart_diagram import generate_flowchart_diagram
from cod8a.generators.mermaid.sequence_diagram import generate_sequence_diagram
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
@click.option('-o', '--output', help='Output file path (saves as .mmd)')
def uml(path, diagram_type, output):
    """Generate UML diagram (Mermaid format)."""
    struct = extract_structure(path)
    base_name = os.path.basename(path or os.getcwd())
    # print(struct)

    if not struct:
        click.echo("Error: Could not extract structure.")
        return

    canon_type = "class"
    if DiagramType.FLOWCHART.value.startswith(diagram_type):
        diagram = generate_flowchart_diagram(struct, base_name)
        canon_type = "flowchart"
    elif DiagramType.SEQUENCE.value.startswith(diagram_type):
        diagram = generate_sequence_diagram(struct)
        canon_type = "sequence"
    else:
        diagram = generate_class_diagram(struct)
        canon_type = "class"
        
    print(diagram)
    
    # Save diagram
    save_diagram(struct, canon_type, diagram, output, path)


# TODO Generating code documentation 
@click.command(hidden=True)
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
