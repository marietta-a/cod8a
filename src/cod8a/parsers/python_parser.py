import ast
import json
import os
from typing import List
from ..models import (
    FileStructure, ClassStructure, MethodStructure, 
    FieldStructure, ParameterStructure, UsingDirective
)
from dataclasses import asdict

class PythonParser:
    def __init__(self):
        self._id_counter = 0

    def _next_id(self):
        self._id_counter += 1
        return self._id_counter

    def parse_file(self, file_path: str) -> FileStructure:
        with open(file_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())

        file_name = os.path.basename(file_path)
        
        file_struct = FileStructure(
            id=self._next_id(), 
            name=file_name, 
            using_directives=[], 
            classes=[], 
            relationships=[]
        )

        for node in tree.body:
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                file_struct.using_directives.extend(self._parse_import(node))
            elif isinstance(node, ast.ClassDef):
                file_struct.classes.append(self._parse_class(node))
        
        data = file_struct.model_dump_json()
        print(data)
        return file_struct

    def _parse_import(self, node) -> List[UsingDirective]:
        directives = []
        if isinstance(node, ast.Import):
            for alias in node.names:
                directives.append(UsingDirective(id=self._next_id(), name=alias.name))
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            for alias in node.names:
                directives.append(UsingDirective(id=self._next_id(), name=f"{module}.{alias.name}"))
        return directives

    def _parse_class(self, node: ast.ClassDef) -> ClassStructure:
        methods = []
        fields = []
        summary = ast.get_docstring(node) or ""

        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                methods.append(self._parse_method(item))
            elif isinstance(item, ast.Assign):
                # Basic field extraction from class-level assignments
                for target in item.targets:
                    if isinstance(target, ast.Name):
                        fields.append(FieldStructure(
                            id=self._next_id(),
                            name=target.id,
                            modifier="public", # Python doesn't have true access modifiers
                            type="", # Type inference is complex, leaving empty for now
                            summary=""
                        ))
            elif isinstance(item, ast.AnnAssign):
                if isinstance(item.target, ast.Name):
                    fields.append(FieldStructure(
                        id=self._next_id(),
                        name=item.target.id,
                        modifier="public",
                        type=ast.unparse(item.annotation),
                        summary=""
                    ))

        return ClassStructure(
            id=self._next_id(),
            name=node.name,
            methods=methods,
            fields=fields,
            type="class",
            summary=summary
        )

    def _parse_method(self, node: ast.FunctionDef) -> MethodStructure:
        summary = ast.get_docstring(node) or ""
        parameters = []
        
        for arg in node.args.args:
            arg_type = ast.unparse(arg.annotation) if arg.annotation else ""
            parameters.append(ParameterStructure(
                name=arg.arg,
                modifier="",
                type=arg_type,
                summary=""
            ))

        return MethodStructure(
            id=self._next_id(),
            name=node.name,
            modifier="public",
            return_type=ast.unparse(node.returns) if node.returns else "",
            parameters=parameters,
            summary=summary
        )

    def parse_project(self, project_path: str) -> List[FileStructure]:
        files = []
        for root, _, filenames in os.walk(project_path):
            for filename in filenames:
                if filename.endswith(".py"):
                    files.append(self.parse_file(os.path.join(root, filename)))
        return files
