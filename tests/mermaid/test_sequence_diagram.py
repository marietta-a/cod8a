import pytest
from cod8a.generators.mermaid.sequence_diagram import SequenceDiagramGenerator
from models.models import FileStructure, ClassStructure

@pytest.fixture
def generator():
    return SequenceDiagramGenerator()

def test_sequence_generator(generator):
    test_data = FileStructure(
        id=1,
        name="test_file.py",
        classes=[
            ClassStructure(id=1, name="Client", type="class", summary="", parent=[], fields=[], methods=[]),
            ClassStructure(id=2, name="Server", type="class", summary="", parent=[], fields=[], methods=[])
        ]
    )

    output = generator.generate(test_data)
    
    assert "sequenceDiagram" in output
    assert "participant Client" in output
    assert "participant Server" in output
    assert "Note over Client, Server: Interaction details not yet extracted from structural JSON." in output
