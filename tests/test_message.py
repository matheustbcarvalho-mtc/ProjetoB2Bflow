from main import MESSAGE_TEMPLATE, build_message
from src.dispara_ai_client import DisparaAiClient


def test_build_message():
    assert build_message("Maria") == "Olá, Maria tudo bem com você?"


def test_message_template_uses_comma_after_ola():
    assert MESSAGE_TEMPLATE == "Olá, {nome} tudo bem com você?"


def test_dispara_ai_client_posts_expected_payload(monkeypatch):
    calls = {}

    class FakeResponse:
        status_code = 202
        content = b'{"id": "abc123", "status": "received"}'
        text = '{"id": "abc123", "status": "received"}'

        def raise_for_status(self):
            return None

        def json(self):
            return {"id": "abc123", "status": "received"}

    def fake_post(url, json, headers, timeout):
        calls["url"] = url
        calls["json"] = json
        calls["headers"] = headers
        calls["timeout"] = timeout
        return FakeResponse()

    monkeypatch.setattr("src.dispara_ai_client.requests.post", fake_post)

    client = DisparaAiClient(
        "https://webhook.dispara.ai/exemplo",
        api_token="token-de-teste",
        timeout=10,
    )
    result = client.send_text("5511999990001", "Olá, Maria tudo bem com você?", name="Maria")

    assert calls == {
        "url": "https://webhook.dispara.ai/exemplo",
        "json": {
            "telefone": "5511999990001",
            "phone": "5511999990001",
            "whatsapp": "5511999990001",
            "mensagem": "Olá, Maria tudo bem com você?",
            "message": "Olá, Maria tudo bem com você?",
            "text": "Olá, Maria tudo bem com você?",
            "nome": "Maria",
            "name": "Maria",
        },
        "headers": {
            "Content-Type": "application/json",
            "Authorization": "Bearer token-de-teste",
        },
        "timeout": 10,
    }
    assert result == {"id": "abc123", "status": "received"}
