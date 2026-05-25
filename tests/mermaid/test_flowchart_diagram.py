import pytest
from cod8a.generators.mermaid.flowchart_diagram import FlowchartDiagramGenerator
from models.models import FileStructure, ClassStructure, ProjectStructure

@pytest.fixture
def generator():
    return FlowchartDiagramGenerator()

def test_flowchart_generator_file(generator):
    test_data = FileStructure(
        id=1,
        name="Models",
        classes=[
            ClassStructure(id=1, name="User", type="class", summary="", associated_item=[], fields=[], methods=[]),
            ClassStructure(id=2, name="Account", type="class", summary="", associated_item=[], fields=[], methods=[])
        ]
    )

    output = generator.generate(test_data)
    
    assert "graph TD" in output
    assert 'file_1["Models"]' in output
    assert 'cls_1["User"]' in output
    assert 'cls_2["Account"]' in output

def test_flowchart_generator_project(generator):
    test_data = ProjectStructure(
        name="TestProject",
        files=[
            FileStructure(
                id=1,
                name="Domain.Models",
                classes=[ClassStructure(id=1, name="Entity", type="class", summary="", associated_item=[], fields=[], methods=[])]
            )
        ]
    )

    output = generator.generate(test_data)
    
    assert "graph TD" in output
    assert 'Project["TestProject"]' in output
    assert 'file_1["Domain.Models"]' in output
    assert 'cls_1["Entity"]' in output
