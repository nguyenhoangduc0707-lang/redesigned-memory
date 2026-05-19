from src.key_manager import audit_keys, classify_value


def test_classify_placeholder():
    status, reason = classify_value("FACEBOOK_PAGE_ACCESS_TOKEN", "your_page_access_token")
    assert status == "placeholder"


def test_classify_present_id():
    status, reason = classify_value("FACEBOOK_PAGE_ID", "123456789")
    assert status == "present"


def test_audit_keys_shape():
    records = audit_keys()
    assert any(record.name == "FACEBOOK_PAGE_ACCESS_TOKEN" for record in records)
    assert all(record.status for record in records)
