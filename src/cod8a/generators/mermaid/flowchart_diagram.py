import re
from typing import List, Union

from cod8a.models.models import FileStructure, ProjectStructure

class FlowchartDiagramGenerator:
    """
    Generates a readable Mermaid flowchart from code structure.
    """

    def generate(self, data: Union['FileStructure', 'ProjectStructure', List['FileStructure']], file_name: str, summarize: bool = False) -> str:
        mermaid_lines = ["graph TD"]

        # Track unique IDs to avoid conflicts in Mermaid
        self.counter = 0

        # Process input
        files =[]
        if isinstance(data, ProjectStructure): files = data.files
        elif isinstance(data, FileStructure): files = [data]
        elif isinstance(data, list): files = data

        for file in files:
            # file_id = f"file_{self._get_id()}"
            file_id = f"file_{file.id}" if file.id else f"file_{self._get_id()}"
            mermaid_lines.append(f'    {file_id}["File: {file.name}"]')

            for cls in file.classes:
                # cls_id = f"cls_{self._get_id()}"
                cls_id = f"cls_{cls.id}" if cls.id else f"cls_{self._get_id()}"
                mermaid_lines.append(f'    {file_id} --> {cls_id}["Class: {cls.name}"]')

                if summarize:
                    continue

                # Exclude private Properties
                fields = [f for f in cls.fields if f.modifier not in "private"]
                # If too many fields, don't overwhelm the diagram truncate
                fields = fields[:10] if len(fields) > 10 else fields
                for field in fields:
                    # f_id = f"f_{self._get_id()}"
                    f_id = f"f_{field.id}" if field.id else f"f_{self._get_id()}"
                    mermaid_lines.append(f'    {cls_id} --> {f_id}["{field.name} ({field.type})"]')

                # Methods: Always helpful to see
                for method in cls.methods:
                    # m_id = f"m_{self._get_id()}"
                    m_id = f"m_{method.id}" if method.id else f"m_{self._get_id()}"
                    mermaid_lines.append(f'    {cls_id} --> {m_id}{{"{method.name}()"}}')

        return "\n".join(mermaid_lines)

    def _get_id(self) -> int:
        self.counter += 1
        return self.counter

def generate_flowchart_diagram(data, file_name, summarize: bool = False) -> str:
    return FlowchartDiagramGenerator().generate(data, file_name, summarize)
