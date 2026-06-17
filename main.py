"""Lê contatos do Supabase e envia mensagem personalizada via Dispara.ai."""

from src.config import Settings
from src.dispara_ai_client import DisparaAiClient
from src.supabase_client import SupabaseContatoRepository

MESSAGE_TEMPLATE = "Olá, {nome} tudo bem com você?"


def build_message(nome: str) -> str:
    return MESSAGE_TEMPLATE.format(nome=nome)


def main() -> None:
    settings = Settings.from_env()

    repository = SupabaseContatoRepository.from_credentials(
        settings.supabase_url,
        settings.supabase_key,
    )
    dispara_ai = DisparaAiClient(
        webhook_url=settings.dispara_webhook_url,
        api_token=settings.dispara_api_token,
    )

    contatos = repository.list_contacts(limit=settings.max_contacts)
    if not contatos:
        print("Nenhum contato encontrado no Supabase.")
        return

    print(f"Enviando mensagens para {len(contatos)} contato(s)...")

    for contato in contatos:
        message = build_message(contato.nome)
        result = dispara_ai.send_text(contato.telefone, message, name=contato.nome)
        status = result.get("id") or result.get("status") or result.get("status_code") or "enviado"
        print(f"✓ {contato.nome} ({contato.telefone}): {status}")


if __name__ == "__main__":
    main()
