import re
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

        # Participants
        for cls in all_classes:
            mermaid_lines.append(f"    participant {cls.name}")
            
        mermaid_lines.append("") 
        
        class_names = {c.name for c in all_classes}
        for cls in all_classes:
            cls_name = cls.name
            
            # Methods
            for method in cls.methods:
                m_name = method.name
                m_type = method.return_type
                
                param_strings = []
                for p in method.parameters:
                     if p.type:
                          param_strings.append(f"{p.name}:{p.type}")
                     else:
                          param_strings.append(p.name)
                p_str = ", ".join(param_strings)
                
                target = cls_name
                for p in method.parameters:
                    if p.type in class_names and p.type != cls_name:
                        target = p.type
                        break
                
                if target == cls_name and m_type in class_names and m_type != cls_name:
                    target = m_type

                interaction = f"    {cls_name}->>{target}: {m_name}({p_str})"
                if m_type and target != cls_name:
                    interaction += f" : {m_type}"
                
                mermaid_lines.append(interaction)
                
            # Fields
            for field in cls.fields:
                match = re.search(r'<([^>]+)>', field.type)
                base_type = match.group(1) if match else field.type
                base_type = base_type.replace('[]', '').strip()
                
                if base_type in class_names and base_type != cls_name:
                    mermaid_lines.append(f"    {cls_name}->>{base_type}: contains {field.name}")

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
