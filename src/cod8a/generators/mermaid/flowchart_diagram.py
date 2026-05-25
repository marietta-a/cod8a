from typing import List, Union

from models.models import ClassStructure, FileStructure, ProjectStructure

class FlowchartDiagramGenerator:
    """
    Generates a Mermaid flowchart diagram from a JSON representation of code structure.
    """

    def generate(self, data: Union[FileStructure, ProjectStructure, List[FileStructure]]) -> str:
        if not isinstance(data, (FileStructure, ProjectStructure, list)):
            return "Error: Invalid data structure"

        mermaid_lines = ["graph TD"]
        
        if isinstance(data, list):
            for file in data:
                mermaid_lines.extend(self._generate_file_subgraph(file))
        elif isinstance(data, ProjectStructure):
            for file in data.files:
                mermaid_lines.extend(self._generate_file_subgraph(file))
        elif isinstance(data, FileStructure):
            mermaid_lines.extend(self._generate_file_subgraph(data))
        
        return "\n".join(mermaid_lines)

    def _generate_file_subgraph(self, file_data: FileStructure) -> List[str]:
        lines = []
        
        if not file_data.classes:
            return lines

        # Clean file name for subgraph ID
        safe_name = "".join(c if c.isalnum() else "_" for c in file_data.name)
        lines.append(f"    subgraph {safe_name}")
        
        for cls in file_data.classes:
            lines.append(f"        {cls.name}[{cls.name}]")
            
        lines.append("    end")
        return lines

def convert_json_to_mermaid_flowchart(data: Union[FileStructure, ProjectStructure]) -> str:
    print("calling uml flowchart generator ...")
    generator = FlowchartDiagramGenerator()
    return generator.generate(data)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            print(convert_json_to_mermaid_flowchart(f.read()))
