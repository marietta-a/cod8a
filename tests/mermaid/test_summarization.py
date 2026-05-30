import pytest
from cod8a.models.models import FileStructure, ClassStructure, MethodStructure, FieldStructure, ParameterStructure
from cod8a.generators.mermaid.class_diagram import ClassDiagramGenerator
from cod8a.generators.mermaid.flowchart_diagram import FlowchartDiagramGenerator
from cod8a.generators.mermaid.sequence_diagram import SequenceDiagramGenerator

@pytest.fixture
def sample_data():
    return FileStructure(
        id=1,
        name="TestFile.py",
        classes=[
            ClassStructure(
                id=1,
                name="TestClass",
                type="class",
                fields=[FieldStructure(id=1, name="field1", modifier="public", type="str", summary="")],
                methods=[MethodStructure(id=1, name="method1", modifier="public", return_type="void", parameters=[], summary="")],
                associated_item=[],
                summary="Sample class"
            )
        ]
    )

def test_class_diagram_summarization(sample_data):
    generator = ClassDiagramGenerator()
    
    # Normal mode
    normal_output = generator.generate(sample_data, summarize=False)
    assert "field1" in normal_output
    assert "method1" in normal_output
    
    # Summarized mode
    summarized_output = generator.generate(sample_data, summarize=True)
    assert "field1" not in summarized_output
    assert "method1" not in summarized_output
    assert "class TestClass" in summarized_output

def test_flowchart_diagram_summarization(sample_data):
    generator = FlowchartDiagramGenerator()
    
    # Normal mode
    normal_output = generator.generate(sample_data, "TestFile", summarize=False)
    assert "field1" in normal_output
    assert "method1" in normal_output
    
    # Summarized mode
    summarized_output = generator.generate(sample_data, "TestFile", summarize=True)
    assert "field1" not in summarized_output
    assert "method1" not in summarized_output
    assert "Class: TestClass" in summarized_output

def test_sequence_diagram_summarization(sample_data):
    generator = SequenceDiagramGenerator()
    
    # We need to make it look like a model or service to trigger interaction logic
    sample_data.classes[0].fields.append(FieldStructure(id=2, name="field2", modifier="public", type="int", summary=""))
    
    # Normal mode
    normal_output = generator.generate(sample_data, summarize=False)
    assert "Set field1" in normal_output
    
    # Summarized mode
    summarized_output = generator.generate(sample_data, summarize=True)
    assert "Set field1" not in summarized_output
    assert "Create TestClass" in summarized_output
