from src.devweb_agent import redact_headers, redact_url, redact_value


def test_redact_headers():
    headers = {
        "authorization": "Bearer secret",
        "content-type": "application/json",
        "cookie": "session=abc",
    }
    redacted = redact_headers(headers)
    assert redacted["authorization"] == "<REDACTED>"
    assert redacted["cookie"] == "<REDACTED>"
    assert redacted["content-type"] == "application/json"


def test_redact_url_query_secrets():
    url = "https://example.com/api?token=abc123&name=test&api_key=secret"
    redacted = redact_url(url)
    assert "token=<REDACTED>" in redacted
    assert "api_key=<REDACTED>" in redacted
    assert "name=test" in redacted


def test_redact_value():
    assert redact_value("abcdef") == "ab***ef"
    assert redact_value("abc") == "***"
