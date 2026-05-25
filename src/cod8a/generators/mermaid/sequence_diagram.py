import re
from typing import List, Union, Set

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
        imports = self._extract_imports(data)
        
        mermaid_lines = ["sequenceDiagram"]
        
        if not all_classes:
            mermaid_lines.append("    participant System")
            return "\n".join(mermaid_lines)

        # 1. Participants
        aliases = {}
        class_names = {c.name for c in all_classes}
        
        client_name = "Client"
        if isinstance(data, ProjectStructure): client_name = "User"
        elif isinstance(data, FileStructure): client_name = "Caller"
        mermaid_lines.append(f"    participant C as {client_name}")
        
        for i, cls in enumerate(all_classes):
            # Initials alias (e.g. PythonParser -> PP)
            alias = "".join([c for c in cls.name if c.isupper()])
            if not alias or alias in aliases.values():
                alias = f"P{i}"
            aliases[cls.name] = alias
            mermaid_lines.append(f"    participant {alias} as {cls.name}")

        external_types = set()
        for imp in imports:
            clean_imp = self._clean_type(imp)
            if clean_imp and clean_imp not in class_names and clean_imp not in self._get_primitive_types():
                external_types.add(clean_imp)

        for i, ext in enumerate(sorted(list(external_types))):
            # Limit external participants to 3 to avoid clutter
            if i >= 3: break
            alias = "".join([c for c in ext if c.isupper()]) or ext[:3].upper()
            if not alias or alias in aliases.values(): alias = f"E{i}"
            aliases[ext] = alias
            mermaid_lines.append(f"    participant {alias} as {ext}")

        mermaid_lines.append("") 

        # 2. Interactions
        for cls in all_classes:
            cls_alias = aliases[cls.name]
            is_behavioral = any(kw in cls.name.lower() for kw in ["parser", "generator", "engine", "service", "cli"])
            
            methods = cls.methods
            if not methods and not cls.fields: continue

            if not is_behavioral:
                # Data classes: Show a single creation flow
                mermaid_lines.append(f"    C->>{cls_alias}: Create {cls.name}")
                for field in cls.fields:
                    base_type = self._clean_type(field.type)
                    if base_type in aliases:
                        mermaid_lines.append(f"    {cls_alias}->>{aliases[base_type]}: Add {field.name}")
                mermaid_lines.append("")
                continue

            # Behavioral classes: Logic-heavy
            # Find the "Main" method (e.g. parse, generate, run)
            main_method = None
            for m in methods:
                if m.name.lower() in ["parse", "generate", "run", "execute", "main"]:
                    main_method = m
                    break
            if not main_method and methods:
                main_method = next((m for m in methods if not m.name.startswith("_")), methods[0])

            if main_method:
                m_name = main_method.name
                params = ", ".join([p.name for p in main_method.parameters if p.name != "self"])
                
                mermaid_lines.append(f"    C->>{cls_alias}: {m_name}({params})")
                mermaid_lines.append(f"    activate {cls_alias}")

                # Heuristic: Alt block for Parser.parse style
                if m_name == "parse" and any(m.name == "parse_project" for m in methods):
                    mermaid_lines.append("    alt is directory")
                    mermaid_lines.append(f"        {cls_alias}->>{cls_alias}: parse_project()")
                    mermaid_lines.append("    else is file")
                    mermaid_lines.append(f"        {cls_alias}->>{cls_alias}: parse_file()")
                    mermaid_lines.append("    end")
                
                # Show external library usage
                for ext_alias in [a for a in aliases.values() if a not in aliases.values() or any(ext in a for ext in ["AST", "LIB", "SYS"])]:
                     if ext_alias != cls_alias and ext_alias != "C" and not any(p.startswith("P") for p in [ext_alias]):
                         # This is a bit loose but tries to find external participants
                         pass

                # Show private methods as self-calls
                for m in methods:
                    if m.name.startswith("_") and m.name != "__init__":
                        mermaid_lines.append(f"    {cls_alias}->>{cls_alias}: {m.name}()")
                
                # Return
                ret = main_method.return_type or "Result"
                mermaid_lines.append(f"    {cls_alias}-->>C: {ret}")
                mermaid_lines.append(f"    deactivate {cls_alias}")
                mermaid_lines.append("")

        return "\n".join(mermaid_lines)

    def _clean_type(self, type_str: str) -> str:
        if not type_str: return ""
        type_str = re.sub(r'[<\[].*?[>\]]', '', type_str)
        return type_str.split('.')[-1].replace('[]', '').replace('?', '').strip()
    
    def _get_primitive_types(self) -> Set[str]:
        return {"int", "string", "str", "bool", "float", "void", "any", "object", "List", "dict", "Optional", "Union", "typing", "models"}

    def _extract_classes(self, data, classes) -> List[ClassStructure]:
        seen = set()
        def add(f):
            for c in f.classes:
                if c.name not in seen:
                    classes.append(c); seen.add(c.name)
        if isinstance(data, FileStructure): add(data)
        elif isinstance(data, ProjectStructure): [add(f) for f in data.files]
        elif isinstance(data, list): [add(item) for item in data if isinstance(item, FileStructure)]
        return classes

    def _extract_imports(self, data) -> Set[str]:
        imps = set()
        def add(f): [imps.add(d.name) for d in (f.using_directives or [])]
        if isinstance(data, FileStructure): add(data)
        elif isinstance(data, ProjectStructure): [add(f) for f in data.files]
        elif isinstance(data, list): [add(i) for i in data if isinstance(i, FileStructure)]
        return imps

def convert_json_to_mermaid_sequence(data: Union[FileStructure, ProjectStructure]) -> str:
    return SequenceDiagramGenerator().generate(data)
