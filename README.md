# Supabase → Dispara.ai · Envio de WhatsApp em Python

Projeto do desafio que **lê contatos cadastrados no Supabase** e dispara, via **webhook da Dispara.ai**, a mensagem:

> **Olá, {nome} tudo bem com você?**

Para até **3 números diferentes** (ou menos, se houver menos contatos no banco).

## Requisitos

- Python 3.11+
- Conta gratuita no [Supabase](https://supabase.com/)
- Conta na [Dispara.ai](https://dispara.ai/) com canal, fluxo e gatilho de webhook ativos

## Estrutura

```
.
├── main.py                      # ponto de entrada
├── src/
│   ├── config.py                # variáveis de ambiente
│   ├── supabase_client.py       # leitura de contatos
│   └── dispara_ai_client.py     # disparo via webhook Dispara.ai
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
| `DISPARA_WEBHOOK_URL` | Dispara.ai → Gatilho de Webhook → Link de Webhook |
| `DISPARA_API_TOKEN` | Opcional: token Bearer caso seu webhook exija autenticação adicional |

No painel da Dispara.ai, crie um fluxo, vincule-o a um gatilho de **Webhook** e configure o mapeamento dos campos recebidos:

| Campo enviado pelo script | Uso sugerido na Dispara.ai |
|---------------------------|----------------------------|
| `telefone`, `phone`, `whatsapp` | Telefone do contato (obrigatório) |
| `nome`, `name`                  | Nome para personalização |
| `mensagem_python`, `saudação`, `saudacao`, `mensagem`, `message`, `text` | Texto pronto da mensagem |

No bloco **Enviar mensagem** do fluxo, selecione o campo `@mensagem_python` para usar a mensagem gerada pelo Python.

## 3. Executar

```bash
python main.py
```

Saída esperada:

```
Enviando mensagens para 3 contato(s)...
✓ Maria (5511999990001): received
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
3. Envia um `POST` JSON para o webhook da Dispara.ai com telefone, nome e mensagem. O payload inclui aliases (`telefone`/`phone`/`whatsapp`, `nome`/`name`, `mensagem_python`/`saudação`/`saudacao`/`mensagem`/`message`/`text`) para facilitar o mapeamento no fluxo.

Referência Dispara.ai: [Integração com GoogleForms](https://ajudadispara.crisp.help/pt-br/article/integracao-com-o-googleforms-1sicagu/)

## Licença

MIT
