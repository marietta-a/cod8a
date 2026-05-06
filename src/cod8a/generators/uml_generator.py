from typing import List, Union
from ..models import FileStructure, ProjectStructure, ClassStructure

class UMLGenerator:
    def generate(self, structure: Union[FileStructure, ProjectStructure]) -> str:
        mermaid_lines = ["classDiagram"]
        
        if isinstance(structure, FileStructure):
            mermaid_lines.extend(self._generate_classes(structure.classes))
        elif isinstance(structure, ProjectStructure):
            for file in structure.files:
                mermaid_lines.extend(self._generate_classes(file.classes))
        
        return "\n".join(mermaid_lines)

    def _generate_classes(self, classes: List[ClassStructure]) -> List[str]:
        lines = []
        for cls in classes:
            lines.append(f"    class {cls.name} {{")
            for field in cls.fields:
                lines.append(f"        {field.type} {field.name}")
            for method in cls.methods:
                params = ", ".join([f"{p.type} {p.name}" for p in method.parameters])
                lines.append(f"        {method.name}({params}) {method.return_type}")
            lines.append("    }")
        return lines
