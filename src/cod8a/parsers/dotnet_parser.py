import subprocess
import json
import os
from typing import Union, List
from models.models import (
    FileStructure, ProjectStructure, ClassStructure, 
    MethodStructure, FieldStructure, ParameterStructure, 
    UsingDirective, Relationship
)

class DotnetParser:
    def __init__(self, analyzer_path: str, file_path: str):
        self.analyzer_path = analyzer_path
        self.file_path = file_path

    def parse(self) -> Union[FileStructure, ProjectStructure]:
        args = ["dotnet", "run", "--project", self.analyzer_path, "--", self.file_path]

        result = subprocess.run(args, capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"Dotnet analyzer failed: {result.stderr}")

        # The C# analyzer might still print some messages to stdout. 
        # We find the last line which should be our JSON.
        lines = result.stdout.strip().splitlines()
        json_str = next((line for line in reversed(lines) if line.startswith('{') and line.endswith('}')), None)
        
        if not json_str:
            raise Exception(f"Could not find JSON in dotnet analyzer output: {result.stdout}")

        data = json.loads(json_str)
        
        if "Files" in data:
            return self._map_project(data)
        return self._map_file(data)

    def _map_project(self, data: dict) -> ProjectStructure:
        return ProjectStructure(
            name=data.get("Name", ""),
            files=[self._map_file(f) for f in data.get("Files", [])]
        )

    def _map_file(self, data: dict) -> FileStructure:
        return FileStructure(
            id=data.get("Id", 0),
            name=data.get("Name", ""),
            using_directives=[UsingDirective(u.get("Id", 0), u.get("Name", "")) for u in data.get("UsingDirectives", []) or []],
            classes=[self._map_class(c) for c in data.get("Classes", []) or []],
            relationships=[Relationship(r.get("Id", 0), r.get("Type", ""), r.get("AssociatedItem", "")) for r in data.get("Relationships", []) or []]
        )

    def _map_class(self, data: dict) -> ClassStructure:
        return ClassStructure(
            id=data.get("Id", 0),
            name=data.get("Name", ""),
            methods=[self._map_method(m) for m in data.get("Methods", []) or []],
            fields=[self._map_field(f) for f in data.get("Fields", []) or []],
            type=data.get("Type", "class"),
            summary=data.get("Summary", "")
        )

    def _map_method(self, data: dict) -> MethodStructure:
        return MethodStructure(
            id=data.get("Id", 0),
            name=data.get("Name", ""),
            modifier=data.get("Modifier", ""),
            return_type=data.get("ReturnType", ""),
            parameters=[ParameterStructure(p.get("Name", ""), p.get("Modifier", ""), p.get("Type", ""), p.get("Summary", "")) for p in data.get("Parameters", []) or []],
            summary=data.get("Summary", "")
        )

    def _map_field(self, data: dict) -> FieldStructure:
        return FieldStructure(
            id=data.get("Id", 0),
            name=data.get("Name", ""),
            modifier=data.get("Modifier", ""),
            type=data.get("Type", ""),
            summary=data.get("Summary", "")
        )
