from src.notebooklm_pro import NotebookLMPro


def test_notebooklm_status_shape():
    client = NotebookLMPro(notebook_id=None)
    status = client.status()
    assert "configured" in status
    assert "cli_available" in status
    assert "export_available" in status


def test_notebooklm_missing_question():
    client = NotebookLMPro(notebook_id=None)
    result = client.ask("")
    assert result["answer"] is None
    assert result["error"] == "Missing question"
