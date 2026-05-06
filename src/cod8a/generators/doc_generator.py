from typing import List, Union
from ..models import FileStructure, ProjectStructure, ClassStructure

class DocGenerator:
    def generate(self, structure: Union[FileStructure, ProjectStructure]) -> str:
        md_lines = []
        
        if isinstance(structure, FileStructure):
            md_lines.append(f"# File: {structure.name}")
            md_lines.extend(self._generate_classes_doc(structure.classes))
        elif isinstance(structure, ProjectStructure):
            md_lines.append(f"# Project: {structure.name}")
            for file in structure.files:
                md_lines.append(f"## File: {file.name}")
                md_lines.extend(self._generate_classes_doc(file.classes))
        
        return "\n".join(md_lines)

    def _generate_classes_doc(self, classes: List[ClassStructure]) -> List[str]:
        lines = []
        for cls in classes:
            lines.append(f"### Class: {cls.name}")
            if cls.summary:
                lines.append(f"{cls.summary}\n")
            
            if cls.fields:
                lines.append("#### Fields")
                for field in cls.fields:
                    lines.append(f"- `{field.modifier} {field.type} {field.name}`: {field.summary}")
                lines.append("")

            if cls.methods:
                lines.append("#### Methods")
                for method in cls.methods:
                    params = ", ".join([f"{p.type} {p.name}" for p in method.parameters])
                    lines.append(f"- `{method.modifier} {method.return_type} {method.name}({params})`")
                    if method.summary:
                        lines.append(f"  - *{method.summary}*")
                lines.append("")
        return lines
