import requests


class ZApiClient:
    BASE_URL = "https://api.z-api.io/instances"

    def __init__(
        self,
        instance_id: str,
        token: str,
        client_token: str | None = None,
        timeout: int = 30,
    ) -> None:
        self._url = f"{self.BASE_URL}/{instance_id}/token/{token}/send-text"
        self._headers = {"Content-Type": "application/json"}
        if client_token:
            self._headers["Client-Token"] = client_token
        self._timeout = timeout

    def send_text(self, phone: str, message: str) -> dict:
        payload = {"phone": phone, "message": message}
        response = requests.post(
            self._url,
            json=payload,
            headers=self._headers,
            timeout=self._timeout,
        )
        response.raise_for_status()
        return response.json()
