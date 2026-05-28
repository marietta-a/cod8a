import os
import re
from typing import Union

import click

from cod8a.parsers.dotnet_parser import DotnetParser
from cod8a.parsers.python_parser import PythonParser
from cod8a.models.models import FileStructure, ProjectStructure

# Path to the C# analyzer project
DOTNET_ANALYZER_PATH = os.path.join(os.path.dirname(__file__), "..", "dotnet", "CodeAnalysis", "CodeAnalyzer.csproj")

def _get_parser(path: str):
    print(f"Checking analyzer ...")
    isDotnetParser = any(path.endswith(ext) for ext in [".cs", ".csproj", ".sln"]) or os.path.isdir(path) and any(f.endswith(".cs") for _, _, files in os.walk(path) for f in files) 
    if isDotnetParser:
        return DotnetParser(DOTNET_ANALYZER_PATH)
    return PythonParser()

# Extracts code structure from the syntax tree
def extract_structure(path) -> Union[FileStructure | ProjectStructure | list[FileStructure]]:
    target = path or os.getcwd()
    parser = _get_parser(target)
    
    pathExists = os.path.exists(path)
    if not pathExists:
        print("Not found")
        return
    
    struct = parser.parse(path or os.getcwd())
    
    return struct

# Save the generated diagram to the directory provided in '-o' command
# or root directory, if no output directory is provided (only on users authorization)
def save_diagram(struct, canon_type, content, output=None, path=None):
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
                # Save in the user's Downloads directory
                save_dir = os.path.join(os.path.expanduser("~"), "Downloads")
                file_path = os.path.join(save_dir, f"{pascal_name}.mmd")
        
        if file_path:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
            with open(file_path, "w") as f:
                f.write(content)
            click.echo(f"Diagram exported to: {file_path}")
            
    except Exception as e:
        click.echo(f"Warning: Could not export diagram: {e}")