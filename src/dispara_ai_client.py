import requests


class DisparaAiClient:
    def __init__(
        self,
        webhook_url: str,
        api_token: str | None = None,
        timeout: int = 30,
    ) -> None:
        self._webhook_url = webhook_url
        self._headers = {"Content-Type": "application/json"}
        if api_token:
            self._headers["Authorization"] = f"Bearer {api_token}"
        self._timeout = timeout

    def send_text(self, phone: str, message: str, name: str | None = None) -> dict:
        payload = {
            "telefone": phone,
            "mensagem": message,
        }
        if name:
            payload["nome"] = name

        response = requests.post(
            self._webhook_url,
            json=payload,
            headers=self._headers,
            timeout=self._timeout,
        )
        response.raise_for_status()

        if not response.content:
            return {"status_code": response.status_code}

        try:
            data = response.json()
        except ValueError:
            return {"status_code": response.status_code, "body": response.text}

        if isinstance(data, dict):
            return data

        return {"status_code": response.status_code, "body": data}
