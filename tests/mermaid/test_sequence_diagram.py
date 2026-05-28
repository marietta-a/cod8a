import pytest
from cod8a.generators.mermaid.sequence_diagram import SequenceDiagramGenerator
from cod8a.models.models import FileStructure, ClassStructure

@pytest.fixture
def generator():
    return SequenceDiagramGenerator()

def test_sequence_generator(generator):
    test_data = FileStructure(
        id=1,
        name="test_file.py",
        classes=[
            ClassStructure(id=1, name="Client", type="class", summary="", associated_item=[], fields=[], methods=[]),
            ClassStructure(id=2, name="Server", type="class", summary="", associated_item=[], fields=[], methods=[])
        ]
    )

    output = generator.generate(test_data)
    
    assert "sequenceDiagram" in output
    assert 'participant C as User' in output
    assert 'participant P0 as "Client"' in output
    assert 'participant P1 as "Server"' in output
