import re
from typing import List, Union

from models.models import ClassStructure, FileStructure, ProjectStructure

class SequenceDiagramGenerator:
    """ Generates a generic Mermaid sequence diagram based on class structure. """

    def _sanitize(self, name: str) -> str:
        return re.sub(r'[^a-zA-Z0-9_ ]', '', name)

    def generate(self, data: Union['FileStructure', 'ProjectStructure', list['FileStructure']]) -> str:
        classes = self._extract_classes(data)
        
        mermaid_lines = ["sequenceDiagram", "    autonumber"]
        
        aliases = {}
        mermaid_lines.append("    participant C as User")
        
        for i, cls in enumerate(classes):
            alias = f"P{i}"
            aliases[cls.name] = alias
            mermaid_lines.append(f'    participant {alias} as "{self._sanitize(cls.name)}"')

        mermaid_lines.append("") 

        # Generic Interaction Logic
        for cls in classes:
            cls_alias = aliases[cls.name]
            
            # Determine if this is a Model or a Service
            # Models have fields, Services have methods
            is_model = len(cls.fields) > len(cls.methods) and len(cls.fields) > 0
            

            if is_model:
                # Do not expose private properties
                fields = [f for f in cls.fields if f.modifier != "private"]
                mermaid_lines.append(f"    C->>{cls_alias}: Create {cls.name}")
                for field in fields[:5]: # Limit to 5 fields to avoid huge diagrams
                    if not field.name.startswith('_'):
                        mermaid_lines.append(f"    {cls_alias}->>{cls_alias}: Set {self._sanitize(field.name)}")
            else:
                # Do not expose private methods
                methods = [m for m in cls.methods if m.modifier != "private"]
                for method in methods:
                    if method.name.lower() in["dispose", "tostring", "equals", "gethashcode", "gettype"]:
                        continue
                    
                    params = ", ".join([p.name for p in method.parameters[:2]])
                    mermaid_lines.append(f"    C->>{cls_alias}: {self._sanitize(method.name)}({params})")
                    
                    # If the method returns something meaningful, show the return
                    ret = self._clean_type(method.return_type)
                    if ret and ret != "void":
                        mermaid_lines.append(f"    {cls_alias}-->>C: {ret}")
            
            mermaid_lines.append("") 

        return "\n".join(mermaid_lines)

    def _extract_classes(self, data) -> List['ClassStructure']:
        # Generic extraction for any input type
        if hasattr(data, 'files'): return [c for f in data.files for c in f.classes]
        if isinstance(data, list): return [c for item in data for c in item.classes]
        if hasattr(data, 'classes'): return data.classes
        return[]

    def _clean_type(self, type_str: str) -> str:
        if not type_str: return ""
        return re.split(r'[<\[]', type_str)[0].replace('?', '').split('.')[-1].strip()

def convert_json_to_mermaid_sequence(data) -> str:
    return SequenceDiagramGenerator().generate(data)