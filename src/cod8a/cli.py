import click
import os
from dataclasses import asdict

from cod8a.generators.mermaid.class_diagram import generate_class_diagram
from cod8a.generators.mermaid.flowchart_diagram import generate_flowchart_diagram
from cod8a.generators.mermaid.sequence_diagram import generate_sequence_diagram
from cod8a.helpers.cli_helper import extract_structure, save_diagram
from cod8a.enums.diagram_type import DiagramType


class ExpandedHelpGroup(click.Group):
    def format_help(self, ctx, formatter):
        # 1. Main help (Group docstring)
        self.format_usage(ctx, formatter)
        self.format_help_text(ctx, formatter)
        self.format_options(ctx, formatter)
        
        # 2. Subcommands and their options
        for command_name in self.list_commands(ctx):
            command = self.get_command(ctx, command_name)
            if command and not command.hidden:
                formatter.write_paragraph()
                with formatter.section(f"Command: {command_name}"):
                    # Usage and help text
                    formatter.write_text(command.help or "")
                    command.format_options(ctx, formatter)

@click.group(cls=ExpandedHelpGroup)
def cli():
    """cod8a (pronounced codetta) is a tool for analyzing and visualizing code structure.
    
    It supports both Python and C# projects, generating Mermaid-compatible diagrams.
    """
    pass

# Generation of UML Diagrams
@cli.command(help="Generate a Mermaid diagram from the source code structure.")
@click.option('-p', '--path', required=True, 
              help='The path to the file or directory to analyze.')
@click.option('-d', '--diagram', 'diagram_type', default='class', 
              type=click.Choice(["seq", "s", "sequence", "flow", "f", "flowchart", "c", "class"]), 
              help='The type of diagram to generate (default: class).')
@click.option('-o', '--output', 
              help='Optional output file path. If not provided, you will be prompted to save to the Downloads folder.')
@click.option('-s', '--summarize', is_flag=True, 
              help='Summarize the diagram by omitting details like fields and methods (recommended for large files).')
def uml(path, diagram_type, output, summarize):
    """Generate UML diagram (Mermaid format)."""
    struct = extract_structure(path)
    base_name = os.path.basename(path or os.getcwd())
    # print(struct)

    if not struct:
        click.echo("Error: Could not extract structure.")
        return

    # Auto-summarize if not explicitly requested
    if not summarize:
        classes = []
        if hasattr(struct, 'files'):
            classes = [c for f in struct.files for c in f.classes]
        elif hasattr(struct, 'classes'):
            classes = struct.classes
        elif isinstance(struct, list):
            classes = [c for f in struct for c in f.classes]
        
        total_members = sum(len(c.fields) + len(c.methods) for c in classes)
        if len(classes) > 50 or total_members > 250:
            click.echo("Note: Large file/project detected. Auto-summarizing diagram for better visualization.")
            summarize = True

    canon_type = "class"
    if DiagramType.FLOWCHART.value.startswith(diagram_type):
        diagram = generate_flowchart_diagram(struct, base_name, summarize)
        canon_type = "flowchart"
    elif DiagramType.SEQUENCE.value.startswith(diagram_type):
        diagram = generate_sequence_diagram(struct, summarize)
        canon_type = "sequence"
    else:
        diagram = generate_class_diagram(struct, summarize)
        canon_type = "class"
        
    print(diagram)
    
    # Save diagram
    save_diagram(struct, canon_type, diagram, output, path)


# # TODO Generating code documentation 
# @click.command(help="[TODO] Generate documentation (Markdown format) from code structure.")
# @click.option('-p', '--path', help='Specific path of file(s) to analyze')
# @click.option('--json', 'output_json', is_flag=True, help='Output in JSON format')
# def doc_cli(path, output_json):
#     """Generate documentation (Markdown format)."""
#     target = path or os.getcwd()
#     struct = extract_structure(target)


# Main entry point for cod8a
def main():
    # cli.add_command(doc_cli, name="doc")
    cli()

# Separate entry point for code8a
# def doc_main():
    # doc_cli()

if __name__ == "__main__":
    main()
