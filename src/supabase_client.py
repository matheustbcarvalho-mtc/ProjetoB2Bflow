from dataclasses import dataclass

from supabase import Client, create_client


@dataclass(frozen=True)
class Contato:
    nome: str
    telefone: str


class SupabaseContatoRepository:
    def __init__(self, client: Client, table_name: str = "contatos") -> None:
        self._client = client
        self._table_name = table_name

    @classmethod
    def from_credentials(cls, url: str, key: str) -> "SupabaseContatoRepository":
        return cls(create_client(url, key))

    def list_contacts(self, limit: int = 3) -> list[Contato]:
        response = (
            self._client.table(self._table_name)
            .select("nome, telefone")
            .order("id")
            .limit(limit)
            .execute()
        )

        contatos: list[Contato] = []
        for row in response.data or []:
            nome = (row.get("nome") or "").strip()
            telefone = _normalize_phone(row.get("telefone") or "")
            if nome and telefone:
                contatos.append(Contato(nome=nome, telefone=telefone))

        return contatos


def _normalize_phone(telefone: str) -> str:
    return "".join(char for char in telefone if char.isdigit())
