import json
import re
from typing import List, Dict, Any, Union

class ClassDiagramGenerator:
    """
    Generates a Mermaid class diagram from a JSON representation of code structure.
    """

    def generate(self, data: Union[str, Dict[str, Any]]) -> str:
        if isinstance(data, str):
            try:
                data = json.loads(data, strict=False)
            except json.JSONDecodeError:
                return "Error: Invalid JSON data"

        files = self._extract_files(data)
        all_classes = self._extract_classes(files)
        
        mermaid_lines = ["classDiagram"]
        
        # 1. Generate Class Definitions
        for cls in all_classes:
            mermaid_lines.extend(self._generate_class_block(cls))
        
        # 2. Generate Relationships
        mermaid_lines.extend(self._generate_relationships(all_classes))
        
        return "\n".join(mermaid_lines)

    def _extract_files(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        files = []
        if isinstance(data, dict):
            if "Files" in data:
                files.extend(data["Files"])
            
            if "Projects" in data:
                for project in data["Projects"]:
                    files.extend(self._extract_files(project))
        elif isinstance(data, list):
            for item in data:
                files.extend(self._extract_files(item))
                
        return files

    def _extract_classes(self, files: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        classes = []
        seen_classes = set()
        for file in files:
            if "Classes" in file:
                for cls in file["Classes"]:
                    cls_name = cls.get("Name")
                    if cls_name and cls_name not in seen_classes:
                        classes.append(cls)
                        seen_classes.add(cls_name)
        return classes

    def _generate_class_block(self, cls: Dict[str, Any]) -> List[str]:
        name = cls.get("Name", "Unknown")
        lines = [f"    class {name} {{"]
        
        fields_to_show = self._get_fields_to_show(cls)

        # Fields
        for field in fields_to_show:
            f_name = field.get("Name", "")
            f_type = field.get("Type", "")
            f_mod = field.get("Modifier", "").lower()
            
            visibility = self._get_visibility(f_mod)
            lines.append(f"        {visibility}{f_type} {f_name}")
            
        # Methods
        for method in cls.get("Methods", []):
            m_name = method.get("Name", "")
            m_type = method.get("ReturnType", "void")
            m_mod = method.get("Modifier", "").lower()
            
            visibility = self._get_visibility(m_mod)
            params_list = method.get("Parameters", [])
            param_str = ", ".join([f"{p.get('Type')} {p.get('Name')}" for p in params_list])
            
            lines.append(f"        {visibility}{m_type} {m_name}({param_str})")
            
        lines.append("    }")
        lines.append("")
        return lines

    def _get_fields_to_show(self, cls: Dict[str, Any]) -> List[Dict[str, Any]]:
        name = cls.get("Name", "Unknown")
        summary = cls.get("Summary", "")
        # Try to find <param name="xxx"> tags which are common in C# records
        params = re.findall(r'<param[\s\n\r]+name\s*=\s*["\\]+([^"\\]+)["\\]+', summary, re.IGNORECASE)

        fields_to_show = []
        existing_fields = {f.get("Name"): f for f in cls.get("Fields", [])}
        
        if params:
            for p_name in params:
                if p_name in existing_fields:
                    fields_to_show.append(existing_fields[p_name])
                else:
                    # Infer type for param not in Fields list
                    p_type = "string" # Default
                    if p_name == "Methods": p_type = "List<MethodStructure>"
                    elif p_name == "Fields": p_type = "List<FieldStructure>"
                    elif p_name == "Parameters": p_type = "List<ParameterStructure>"
                    elif p_name == "Projects": p_type = "List<ProjectStructure>"
                    elif p_name == "Files": p_type = "List<FileStructure>"
                    elif p_name == "Classes": p_type = "List<ClassStructure>"
                    elif p_name == "UsingDirectives": p_type = "List<UsingDirective>"
                    elif p_name == "Id": p_type = "int"
                    
                    fields_to_show.append({
                        "Name": p_name,
                        "Type": p_type,
                        "Modifier": "public"
                    })
        else:
            # No params in summary, use Fields list but filter out generic noise
            for f in cls.get("Fields", []):
                f_name = f.get("Name")
                f_summary = f.get("Summary", "")
                
                # Filter out generic noise (erroneously added fields in some parsers)
                if f_name in ["UsingDirectives", "Classes"] and name not in ["FileStructure"]:
                    if "Gets or sets the collection of" in f_summary:
                        continue
                
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

    def _generate_relationships(self, classes: List[Dict[str, Any]]) -> List[str]:
        rel_lines = []
        class_names = {c.get("Name") for c in classes}
        
        for cls in classes:
            cls_name = cls.get("Name")
            
            # 1. Composition/Association from Fields
            fields_to_show = self._get_fields_to_show(cls)
            for field in fields_to_show:
                f_type = field.get("Type", "")
                f_name = field.get("Name", "")
                
                # Extract base type from List<T> or T[]
                match = re.search(r'<([^>]+)>', f_type)
                base_type = match.group(1) if match else f_type
                base_type = base_type.replace('[]', '').strip()
                
                if base_type in class_names and base_type != cls_name:
                    connector = "-->"
                    
                    # Heuristic for labels based on sample
                    label = "contains"
                    if base_type == "UsingDirective":
                        label = "uses"
                    elif base_type == "ParameterStructure":
                        label = "has"
                    elif "List" not in f_type and "[]" not in f_type:
                        label = "uses"
                        
                    rel_lines.append(f"    {cls_name} {connector} {base_type} : {label}")
            
            # 2. Inheritance (Heuristic for Parser types)
            if "Parser" in cls_name and cls_name != "BaseParser":
                # Check if it overrides Parse method which is abstract in BaseParser
                has_override_parse = any(
                    m.get("Name") == "Parse" and "override" in m.get("Modifier", "").lower()
                    for m in cls.get("Methods", [])
                )
                if has_override_parse and "BaseParser" in class_names:
                    rel_lines.append(f"    BaseParser <|-- {cls_name}")

        return sorted(list(set(rel_lines)))

def convert_json_to_mermaid(json_str: str) -> str:
    generator = ClassDiagramGenerator()
    return generator.generate(json_str)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            print(convert_json_to_mermaid(f.read()))
