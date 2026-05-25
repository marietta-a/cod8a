import re
from typing import List, Union

from models.models import ClassStructure, FileStructure, ProjectStructure

class FlowchartDiagramGenerator:
    """
    Generates a Mermaid flowchart diagram from a representation of code structure.
    """

    def generate(self, data: Union[FileStructure, ProjectStructure, List[FileStructure]]) -> str:
        if not isinstance(data, (FileStructure, ProjectStructure, list)):
            return "Error: Invalid data structure"

        mermaid_lines = ["graph TD"]
        
        if isinstance(data, ProjectStructure):
            mermaid_lines.append(f'    Project["{data.name}"]')
            for file in data.files:
                file_id = f"file_{file.id}"
                mermaid_lines.append(f'    Project --> {file_id}["{file.name}"]')
                mermaid_lines.extend(self._generate_file_content(file, file_id))
        elif isinstance(data, FileStructure):
            file_id = f"file_{data.id}"
            mermaid_lines.append(f'    {file_id}["{data.name}"]')
            mermaid_lines.extend(self._generate_file_content(data, file_id))
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, FileStructure):
                    file_id = f"file_{item.id}"
                    mermaid_lines.append(f'    {file_id}["{item.name}"]')
                    mermaid_lines.extend(self._generate_file_content(item, file_id))
            
        return "\n".join(mermaid_lines)

    def _generate_file_content(self, file_data: FileStructure, file_id: str) -> List[str]:
        lines = []
        
        if not file_data.classes:
            return lines

        for cls in file_data.classes:
            cls_id = f"cls_{cls.id}"
            lines.append(f'    {file_id} --> {cls_id}["{cls.name}"]')
            
            # Optionally add methods and fields as sub-nodes
            if cls.methods or cls.fields:
                lines.append(f'    subgraph {cls.name}_Components')
                for field in cls.fields:
                    f_id = f"field_{field.id}"
                    lines.append(f'        {cls_id} --> {f_id}["{field.name}"]')
                for method in cls.methods:
                    m_id = f"method_{method.id}"
                    lines.append(f'        {cls_id} --> {m_id}["{method.name}()"]')
                lines.append('    end')

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
