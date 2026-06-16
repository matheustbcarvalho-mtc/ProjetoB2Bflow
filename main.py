"""Lê contatos do Supabase e envia mensagem personalizada via Z-API."""

from src.config import Settings
from src.supabase_client import SupabaseContatoRepository
from src.zapi_client import ZApiClient

MESSAGE_TEMPLATE = "Olá, {nome} tudo bem com você?"


def build_message(nome: str) -> str:
    return MESSAGE_TEMPLATE.format(nome=nome)


def main() -> None:
    settings = Settings.from_env()

    repository = SupabaseContatoRepository.from_credentials(
        settings.supabase_url,
        settings.supabase_key,
    )
    zapi = ZApiClient(
        instance_id=settings.zapi_instance_id,
        token=settings.zapi_token,
        client_token=settings.zapi_client_token,
    )

    contatos = repository.list_contacts(limit=settings.max_contacts)
    if not contatos:
        print("Nenhum contato encontrado no Supabase.")
        return

    print(f"Enviando mensagens para {len(contatos)} contato(s)...")

    for contato in contatos:
        message = build_message(contato.nome)
        result = zapi.send_text(contato.telefone, message)
        print(f"✓ {contato.nome} ({contato.telefone}): {result.get('messageId', 'enviado')}")


if __name__ == "__main__":
    main()
