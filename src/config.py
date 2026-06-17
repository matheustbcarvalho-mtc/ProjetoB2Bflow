import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    supabase_url: str
    supabase_key: str
    dispara_webhook_url: str
    dispara_api_token: str | None
    max_contacts: int

    @classmethod
    def from_env(cls) -> "Settings":
        missing = [
            name
            for name, value in {
                "SUPABASE_URL": os.getenv("SUPABASE_URL"),
                "SUPABASE_KEY": os.getenv("SUPABASE_KEY"),
                "DISPARA_WEBHOOK_URL": os.getenv("DISPARA_WEBHOOK_URL"),
            }.items()
            if not value
        ]
        if missing:
            raise ValueError(f"Variáveis de ambiente obrigatórias ausentes: {', '.join(missing)}")

        max_contacts = int(os.getenv("MAX_CONTACTS", "3"))

        return cls(
            supabase_url=os.environ["SUPABASE_URL"],
            supabase_key=os.environ["SUPABASE_KEY"],
            dispara_webhook_url=os.environ["DISPARA_WEBHOOK_URL"],
            dispara_api_token=os.getenv("DISPARA_API_TOKEN") or None,
            max_contacts=max(1, min(max_contacts, 3)),
        )
