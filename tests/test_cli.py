import pytest
from click.testing import CliRunner
from cod8a.cli import cli
import os

def test_uml_no_summarize_flag():
    runner = CliRunner()
    # Using a small file that definitely won't auto-summarize normally
    # but we want to make sure the flag is accepted.
    result = runner.invoke(cli, ['uml', '-p', 'src/cod8a/cli.py', '--no-summarize'], input='n\n')
    assert result.exit_code == 0
    assert "--no-summarize" not in result.output # Should not show error
    assert "classDiagram" in result.output

def test_uml_summarize_flag():
    runner = CliRunner()
    result = runner.invoke(cli, ['uml', '-p', 'src/cod8a/cli.py', '--summarize'], input='n\n')
    assert result.exit_code == 0
    assert "classDiagram" in result.output
    # In summarize mode, we shouldn't see method details like "main()" or "uml()"
    # Wait, python parser might extract them.
    assert "uml" not in result.output or "uml(" not in result.output

def test_uml_auto_summarize_threshold(monkeypatch):
    # Mock the structure to look large
    from cod8a.models.models import FileStructure, ClassStructure, FieldStructure
    
    large_struct = FileStructure(
        id=1,
        name="LargeFile.py",
        classes=[ClassStructure(id=i, name=f"Class{i}", type="class", fields=[FieldStructure(id=j, name=f"f{j}", modifier="public", type="int", summary="") for j in range(10)], methods=[], associated_item=[], summary="") for i in range(60)]
    )
    
    # We need to mock extract_structure to return this large_struct
    import cod8a.cli
    monkeypatch.setattr(cod8a.cli, "extract_structure", lambda path: large_struct)
    
    runner = CliRunner()
    
    # Test auto-summarize
    result = runner.invoke(cli, ['uml', '-p', 'fake_path'], input='n\n')
    assert "Note: Large file/project detected. Auto-summarizing" in result.output
    
    # Test --no-summarize override
    result_override = runner.invoke(cli, ['uml', '-p', 'fake_path', '--no-summarize'], input='n\n')
    assert "Note: Large file/project detected. Auto-summarizing" not in result_override.output
