import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    supabase_url: str
    supabase_key: str
    zapi_instance_id: str
    zapi_token: str
    zapi_client_token: str | None
    max_contacts: int

    @classmethod
    def from_env(cls) -> "Settings":
        missing = [
            name
            for name, value in {
                "SUPABASE_URL": os.getenv("SUPABASE_URL"),
                "SUPABASE_KEY": os.getenv("SUPABASE_KEY"),
                "ZAPI_INSTANCE_ID": os.getenv("ZAPI_INSTANCE_ID"),
                "ZAPI_TOKEN": os.getenv("ZAPI_TOKEN"),
            }.items()
            if not value
        ]
        if missing:
            raise ValueError(f"Variáveis de ambiente obrigatórias ausentes: {', '.join(missing)}")

        max_contacts = int(os.getenv("MAX_CONTACTS", "3"))

        return cls(
            supabase_url=os.environ["SUPABASE_URL"],
            supabase_key=os.environ["SUPABASE_KEY"],
            zapi_instance_id=os.environ["ZAPI_INSTANCE_ID"],
            zapi_token=os.environ["ZAPI_TOKEN"],
            zapi_client_token=os.getenv("ZAPI_CLIENT_TOKEN"),
            max_contacts=max(1, min(max_contacts, 3)),
        )
