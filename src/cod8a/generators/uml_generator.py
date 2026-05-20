from typing import List, Union
from enums.diagram_type import DiagramType
from models.models import FileStructure, ProjectStructure, ClassStructure, Relationship

class UMLGenerator:
    def generate(self, structure: Union[FileStructure, ProjectStructure], diagram_type: DiagramType = DiagramType.CLASS) -> str:
        if diagram_type == DiagramType.CLASS:
            return self._generate_class_diagram(structure)
        elif diagram_type == DiagramType.FLOWCHART:
            return self._generate_flowchart(structure)
        elif diagram_type == DiagramType.SEQUENCE:
            return self._generate_sequence_diagram(structure)
        else:
            return self._generate_class_diagram(structure)

    def _generate_class_diagram(self, structure: Union[FileStructure, ProjectStructure]) -> str:
        mermaid_lines = ["classDiagram"]
        
        if isinstance(structure, FileStructure):
            mermaid_lines.extend(self._generate_classes(structure.classes))
            mermaid_lines.extend(self._generate_relationships(structure.relationships))
        elif isinstance(structure, ProjectStructure):
            for file in structure.files:
                mermaid_lines.extend(self._generate_classes(file.classes))
                mermaid_lines.extend(self._generate_relationships(file.relationships))
        
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

    def _generate_relationships(self, relationships: List[Relationship]) -> List[str]:
        lines = []
        if not relationships:
            return lines
        for rel in relationships:
            # Simple mapping of relationships for Mermaid
            # rel.type could be "inheritance", "composition", etc.
            connector = "-->"
            rel_type = rel.type.lower() if rel.type else ""
            if rel_type == "inheritance":
                connector = "--|>"
            elif rel_type == "composition":
                connector = "--*"
            
            # This is a bit naive as we don't know the source of the relationship here easily
            # without more context. For now, we skip if we can't determine it.
            pass
        return lines

    def _generate_flowchart(self, structure: Union[FileStructure, ProjectStructure]) -> str:
        lines = ["graph TD"]
        if isinstance(structure, FileStructure):
            lines.append(f"    subgraph {structure.name}")
            for cls in structure.classes:
                lines.append(f"        {cls.name}[{cls.name}]")
            lines.append("    end")
        elif isinstance(structure, ProjectStructure):
            for file in structure.files:
                lines.append(f"    subgraph {file.name}")
                for cls in file.classes:
                    lines.append(f"        {cls.name}[{cls.name}]")
                lines.append("    end")
        return "\n".join(lines)

    def _generate_sequence_diagram(self, structure: Union[FileStructure, ProjectStructure]) -> str:
        lines = ["sequenceDiagram"]
        # Very basic sequence diagram placeholder
        if isinstance(structure, FileStructure):
            for cls in structure.classes:
                lines.append(f"    participant {cls.name}")
        elif isinstance(structure, ProjectStructure):
            for file in structure.files:
                for cls in file.classes:
                    lines.append(f"    participant {cls.name}")
        
        lines.append("    Note over User, System: Interaction details not yet extracted")
        return "\n".join(lines)
