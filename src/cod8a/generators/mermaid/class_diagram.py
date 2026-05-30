import json
import re
from typing import List, Dict, Any, Union

from cod8a.models.models import ClassStructure, FieldStructure, FileStructure, ProjectStructure

class ClassDiagramGenerator:
    """
    Generates a Mermaid class diagram from a JSON representation of code structure.
    """

    def generate(self, data: Union[FileStructure, ProjectStructure, List[FileStructure]], summarize: bool = False) -> str:
        if not isinstance(data, FileStructure | ProjectStructure | list):
                return "Error: Invalid data structure"

        # files = self._extract_files(data)
        classes = []
        all_classes = self._extract_classes(data, classes)
        mermaid_lines = ["classDiagram"]
        # 1. Generate Class Definitions
        for cls in all_classes:
            mermaid_lines.extend(self._generate_class_block(cls, summarize))
        
        # 2. Generate Relationships
        mermaid_lines.extend(self._generate_relationships(all_classes))
        
        return "\n".join(mermaid_lines)

    def _extract_files(self, data: Union[FileStructure | ProjectStructure]) -> List[Union[FileStructure | ProjectStructure]]:
        files : list[FileStructure] = []
        if isinstance(data, FileStructure):
            if "files" in data:
                for file in data["files"]:
                    files.extend(file)
            
            else:
                files.extend(data)
                
        return files

    def _extract_classes(self, data: Union[FileStructure | ProjectStructure], classes: list[ClassStructure]) -> List[ClassStructure]:
        seen_classes = set()
        if isinstance(data, FileStructure):
            for cls in data.classes:
                cls_name = cls.name
                if cls_name and cls_name not in seen_classes:
                    classes.append(cls)
                    seen_classes.add(cls_name)
        elif isinstance(data, list):
            for file in data:
                self._extract_classes(file, classes)
        elif isinstance(data, ProjectStructure):
            for file in data.files:
              self._extract_classes(file, classes)
        else:
            print("Invalid file structure")
            return 
        
        return classes

    def _generate_class_block(self, cls: ClassStructure, summarize: bool = False) -> List[str]:
        if summarize:
            return [f"    class {cls.name}", ""]
            
        lines = [f"    class {cls.name} {{"]
        
        # Fields
        for field in cls.fields:
            f_name = field.name
            f_type = field.type
            f_mod = field.modifier.lower()
            
            visibility = self._get_visibility(f_mod)
            lines.append(f"        {visibility}{f_type} {f_name}")
            
        # Methods
        for method in cls.methods:
            m_name = method.name
            m_type = method.return_type
            m_mod = method.modifier.lower()
            
            visibility = self._get_visibility(m_mod)
            params_list = method.parameters
            param_str = ", ".join([f"{p.type} {p.name}" if p.type else p.name for p in params_list])
            
            method_line = f"        {visibility}{m_name}({param_str})"
            if m_type:
                method_line += f" {m_type}"
            lines.append(method_line)
            
        lines.append("    }")
        lines.append("")
        return lines

    def _get_fields_to_show(self, cls: ClassStructure) -> List[FieldStructure]:
        # Try to find <param name="xxx"> tags which are common in C# records
        params = re.findall(r'<param[\s\n\r]+name\s*=\s*["\\]+([^"\\]+)["\\]+', cls.summary, re.IGNORECASE)

        fields_to_show = []
        existing_fields = {f.name: f for f in cls.fields}
        
        if params:
            for p_name in params:
                if p_name in existing_fields:
                    fields_to_show.append(existing_fields[p_name])
        else:
            # No params in summary
            for f in cls.fields:
                fields_to_show.append(f)
        return fields_to_show

    def _get_visibility(self, modifier: str) -> str:
        if "public" in modifier:
            return "+"
        if "private" in modifier:
            return "-"
        if "protected" in modifier:
            return "#"
        if "internal" in modifier:
            return "~"
        return "+" # Default to public

    def _generate_relationships(self, classes: List[ClassStructure]) -> List[str]:
        rel_lines = []
        class_names = {c.name for c in classes}
        
        for cls in classes:
            cls_name = cls.name
            # Check for inheritance/implementation
            for relation in cls.associated_item:
                connector = "<|--" # Default to inheritance
                label = "inherits"
                if "interface" in relation.type.lower() or "implements" in relation.type.lower():
                   label = "implements"
                elif "extension" in relation.type.lower():
                    label = "extends"
                    connector = "<.."
                
                rel_lines.append(f"    {relation.parent_name} {connector} {cls_name} : {label}")
            
            # Composition/Association from Fields
            for field in cls.fields:
                # Extract base type from List<T> or T[]
                match = re.search(r'<([^>]+)>', field.type)
                base_type = match.group(1) if match else field.type
                base_type = base_type.replace('[]', '').strip()
                
                for name in class_names:
                    if name in base_type and cls_name != name:
                        connector = "-->"
                        label = "uses"
                        
                        # Use composition for collections if it looks like it contains the class
                        if "List" in field.type or "[]" in field.type:
                            connector = "*--"
                            label = "contains"
                        
                        rel_lines.append(f"    {cls_name} {connector} {name} : {label}")
                    
        return sorted(list(set(rel_lines)))

def generate_class_diagram(data: FileStructure | ProjectStructure, summarize: bool = False) -> str:
    print("calling uml class generator ...")
    generator = ClassDiagramGenerator()
    return generator.generate(data, summarize)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            print(generate_class_diagram(f.read()))
