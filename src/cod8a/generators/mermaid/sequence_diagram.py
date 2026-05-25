from typing import List, Union

from models.models import ClassStructure, FileStructure, ProjectStructure

class SequenceDiagramGenerator:
    """
    Generates a Mermaid sequence diagram from a JSON representation of code structure.
    """

    def generate(self, data: Union[FileStructure, ProjectStructure, List[FileStructure]]) -> str:
        if not isinstance(data, (FileStructure, ProjectStructure, list)):
            return "Error: Invalid data structure"

        classes = []
        all_classes = self._extract_classes(data, classes)
        
        mermaid_lines = ["sequenceDiagram"]
        
        if not all_classes:
            return "\n".join(mermaid_lines)

        participants = [cls.name for cls in all_classes]
        
        for p in participants:
            mermaid_lines.append(f"    participant {p}")
            
        if len(participants) > 1:
            participants_str = ", ".join(participants[:2]) if len(participants) >= 2 else participants[0]
            mermaid_lines.append(f"    Note over {participants_str}: Interaction details not yet extracted from structural JSON.")
        elif participants:
             mermaid_lines.append(f"    Note over {participants[0]}: Interaction details not yet extracted from structural JSON.")

        return "\n".join(mermaid_lines)

    def _extract_classes(self, data: Union[FileStructure, ProjectStructure, List[FileStructure]], classes: list[ClassStructure]) -> List[ClassStructure]:
        seen_classes = set()
        
        def add_classes_from_file(file_data: FileStructure):
            for cls in file_data.classes:
                if cls.name and cls.name not in seen_classes:
                    classes.append(cls)
                    seen_classes.add(cls.name)

        if isinstance(data, FileStructure):
             add_classes_from_file(data)
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, FileStructure):
                     add_classes_from_file(item)
        elif isinstance(data, ProjectStructure):
            for file in data.files:
                 add_classes_from_file(file)
        
        return classes

def convert_json_to_mermaid_sequence(data: Union[FileStructure, ProjectStructure]) -> str:
    print("calling uml sequence generator ...")
    generator = SequenceDiagramGenerator()
    return generator.generate(data)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            print(convert_json_to_mermaid_sequence(f.read()))
