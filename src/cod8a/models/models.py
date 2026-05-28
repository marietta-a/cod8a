from typing import List, Optional

from pydantic import BaseModel, Field
from pydantic.dataclasses import dataclass

@dataclass
class UsingDirective:
    id: int
    name: str

@dataclass
class ParameterStructure:
    name: str
    modifier: str
    type: str
    summary: str

@dataclass
class FieldStructure:
    id: int
    name: str
    modifier: str
    type: str
    summary: str

@dataclass
class MethodStructure:
    id: int
    name: str
    modifier: str
    return_type: str
    parameters: List[ParameterStructure]
    summary: str

@dataclass
class Relationship:
    id: int
    type: str
    parent_name: str

@dataclass
class ClassStructure:
    id: int
    name: str
    methods: List[MethodStructure]
    fields: List[FieldStructure]
    type: str
    associated_item: List[Relationship]
    summary: str

class FileStructure(BaseModel):
    id: int
    name: str
    using_directives: Optional[List[UsingDirective]] = []
    classes: Optional[List[ClassStructure]] = []


class ProjectStructure(BaseModel):
    name: str
    files: List[FileStructure] = []
