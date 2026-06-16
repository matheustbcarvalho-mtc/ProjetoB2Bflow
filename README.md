# Supabase → Z-API · Envio de WhatsApp em Python

Projeto do desafio que **lê contatos cadastrados no Supabase** e envia, via **Z-API**, a mensagem:

> **Olá, {nome} tudo bem com você?**

Para até **3 números diferentes** (ou menos, se houver menos contatos no banco).

## Requisitos

- Python 3.11+
- Conta gratuita no [Supabase](https://supabase.com/)
- Conta/instância gratuita na [Z-API](https://z-api.io/) com WhatsApp conectado

## Estrutura

```
.
├── main.py                      # ponto de entrada
├── src/
│   ├── config.py                # variáveis de ambiente
│   ├── supabase_client.py       # leitura de contatos
│   └── zapi_client.py           # envio via Z-API
├── supabase/migrations/         # SQL da tabela contatos
├── tests/                       # testes da mensagem
├── requirements.txt
└── .env.example
```

## 1. Banco de dados (Supabase)

Execute o SQL em `supabase/migrations/001_create_contatos.sql` no **SQL Editor** do Supabase, ou use a CLI:

```bash
supabase db push
```

A tabela `contatos` possui:

| Coluna    | Tipo | Descrição                          |
|-----------|------|------------------------------------|
| `nome`    | text | Nome usado na personalização       |
| `telefone`| text | Número com DDI+DDD (só dígitos)    |

**Importante:** substitua os telefones de exemplo pelos números reais antes de enviar.

## 2. Configuração

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
```

Preencha o `.env`:

| Variável            | Onde encontrar                                      |
|---------------------|-----------------------------------------------------|
| `SUPABASE_URL`      | Supabase → Settings → API → Project URL             |
| `SUPABASE_KEY`      | Supabase → Settings → API → anon key (ou service_role para scripts locais) |
| `ZAPI_INSTANCE_ID`  | Z-API → Instâncias                                  |
| `ZAPI_TOKEN`        | Z-API → Instâncias → Token                          |
| `ZAPI_CLIENT_TOKEN` | Z-API → Segurança (opcional)                        |

## 3. Executar

```bash
python main.py
```

Saída esperada:

```
Enviando mensagens para 3 contato(s)...
✓ Maria (5511999990001): D241XXXX732339502B68
✓ João (5511999990002): ...
✓ Ana (5511999990003): ...
```

## 4. Testes

```bash
pip install pytest
pytest
```

## Como funciona

1. O script busca até `MAX_CONTACTS` registros (padrão 3) na tabela `contatos`.
2. Para cada contato, monta a mensagem: `Olá, {nome} tudo bem com você?`
3. Envia via endpoint Z-API `POST /instances/{id}/token/{token}/send-text`.

Documentação Z-API: [Enviar texto simples](https://developer.z-api.io/message/send-text)

## Licença

MIT
