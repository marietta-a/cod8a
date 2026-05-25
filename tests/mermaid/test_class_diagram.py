import pytest
from cod8a.generators.mermaid.class_diagram import ClassDiagramGenerator
from models.models import (
    FileStructure, ClassStructure, FieldStructure, 
    MethodStructure, ParameterStructure, Relationship
)

@pytest.fixture
def generator():
    return ClassDiagramGenerator()

def test_generate_class_diagram_basic(generator):
    # Arrange
    test_data = FileStructure(
        id=1,
        name="test_file.py",
        using_directives=[],
        classes=[
            ClassStructure(
                id=1,
                name="User",
                type="class",
                summary="A user class",
                parent=[
                    Relationship(id=1, type="Class", associated_item="BaseEntity")
                ],
                fields=[
                    FieldStructure(id=1, name="username", modifier="private", type="str", summary=""),
                    FieldStructure(id=2, name="role", modifier="public", type="Role", summary="")
                ],
                methods=[
                    MethodStructure(
                        id=1, 
                        name="login", 
                        modifier="public", 
                        return_type="bool", 
                        summary="",
                        parameters=[
                            ParameterStructure(name="password", modifier="", type="str", summary="")
                        ]
                    )
                ]
            ),
            ClassStructure(
                id=2,
                name="Role",
                type="class",
                summary="Role class",
                parent=[],
                fields=[],
                methods=[]
            )
        ]
    )

    # Act
    mermaid_output = generator.generate(test_data)

    # Assert
    assert "classDiagram" in mermaid_output
    assert "class User {" in mermaid_output
    assert "-str username" in mermaid_output
    assert "+Role role" in mermaid_output
    assert "+bool login(str password)" in mermaid_output
    
    # Check relationships
    assert "BaseEntity <|.. User  : inherits" in mermaid_output or "User <|.. BaseEntity" in mermaid_output or "BaseEntity <|.. User" in mermaid_output
    assert "User --> Role : uses" in mermaid_output or "User --> Role : contains" in mermaid_output
