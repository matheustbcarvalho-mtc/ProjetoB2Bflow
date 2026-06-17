# Supabase + Dispara.ai: envio de WhatsApp em Python

Este projeto lê contatos cadastrados no Supabase e aciona um gatilho de webhook da Dispara.ai para enviar mensagens de WhatsApp personalizadas.

Mensagem enviada para cada contato:

> Olá, {nome} tudo bem com você?

Por segurança, o script envia no máximo 3 contatos por execução. Esse limite pode ser ajustado pela variável `MAX_CONTACTS`, mas o código sempre restringe o valor ao intervalo de 1 a 3.

## Requisitos

- Python 3.11+
- Projeto no [Supabase](https://supabase.com/)
- Conta na [Dispara.ai](https://dispara.ai/)
- Canal de WhatsApp conectado na Dispara.ai
- Fluxo da Dispara.ai com bloco **Enviar mensagem**
- Gatilho de webhook ativo na Dispara.ai, vinculado ao fluxo

## Estrutura

```text
.
├── main.py
├── src/
│   ├── config.py
│   ├── dispara_ai_client.py
│   └── supabase_client.py
├── supabase/migrations/
│   └── 001_create_contatos.sql
├── tests/
│   └── test_message.py
├── .env.example
└── requirements.txt
```

## 1. Configurar o Supabase

Execute a migration em `supabase/migrations/001_create_contatos.sql` no SQL Editor do Supabase ou pela CLI:

```bash
supabase db push
```

A tabela usada pelo script é `public.contatos`:

| Coluna | Descrição |
| --- | --- |
| `nome` | Nome usado para personalizar a mensagem |
| `telefone` | Número do WhatsApp com DDI + DDD + número, usando apenas dígitos |

Exemplo de telefone válido:

```text
5537999999461
```

## 2. Configurar a Dispara.ai

No painel da Dispara.ai:

1. Conecte o canal de WhatsApp.
2. Crie um fluxo.
3. Adicione um bloco **Enviar mensagem**.
4. Crie um gatilho do tipo **Webhook**.
5. Vincule o gatilho ao fluxo.
6. Copie o link do webhook para usar em `DISPARA_WEBHOOK_URL`.
7. Envie uma requisição de teste para o webhook.
8. No gatilho, mapeie os campos recebidos do JSON para os campos da Dispara.ai.

O script envia este payload para o webhook:

```json
{
  "telefone": "5537999999461",
  "phone": "5537999999461",
  "whatsapp": "5537999999461",
  "nome": "Maria",
  "name": "Maria",
  "mensagem_python": "Olá, Maria tudo bem com você?",
  "mensagem": "Olá, Maria tudo bem com você?",
  "message": "Olá, Maria tudo bem com você?",
  "text": "Olá, Maria tudo bem com você?",
  "saudacao": "Olá, Maria tudo bem com você?",
  "saudação": "Olá, Maria tudo bem com você?"
}
```

Mapeamento recomendado na Dispara.ai:

| Campo recebido no webhook | Campo na Dispara.ai |
| --- | --- |
| `body.telefone` ou `body.whatsapp` | Telefone/WhatsApp do contato |
| `body.nome` | Nome do contato |
| `body.mensagem_python` | Campo personalizado `mensagem_python` |

No bloco **Enviar mensagem** do fluxo, selecione o campo personalizado `mensagem_python` pelo menu de variáveis da Dispara.ai. Não digite `@mensagem_python` manualmente como texto comum; selecione a variável exibida pela interface.

## 3. Configurar o ambiente local

Crie e ative um ambiente virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Crie o `.env`:

```bash
cp .env.example .env
```

Preencha as variáveis:

```env
SUPABASE_URL=https://SEU_PROJETO.supabase.co
SUPABASE_KEY=sua_chave_anon_ou_service_role

DISPARA_WEBHOOK_URL=https://link.dispara.ai/w/SEU_WEBHOOK
DISPARA_API_TOKEN=

MAX_CONTACTS=3
```

Variáveis:

| Variável | Obrigatória | Descrição |
| --- | --- | --- |
| `SUPABASE_URL` | Sim | URL do projeto Supabase |
| `SUPABASE_KEY` | Sim | Chave anon ou service role para o script local |
| `DISPARA_WEBHOOK_URL` | Sim | Link do webhook do gatilho da Dispara.ai |
| `DISPARA_API_TOKEN` | Não | Token Bearer opcional, se o webhook exigir autenticação |
| `MAX_CONTACTS` | Não | Quantidade de contatos por execução, limitada de 1 a 3 |

## 4. Executar

Para enviar para a quantidade configurada em `MAX_CONTACTS`:

```bash
python3 main.py
```

Para testar com apenas 1 contato:

```bash
MAX_CONTACTS=1 python3 main.py
```

Saída esperada:

```text
Enviando mensagens para 1 contato(s)...
✓ Maria (5537999999461): 204
```

O status `204` indica que a Dispara.ai recebeu o webhook com sucesso. A entrega no WhatsApp depende do fluxo, do canal conectado e do mapeamento dos campos no painel da Dispara.ai.

## 5. Testes

```bash
python3 -m pytest
```

## Como funciona

1. `main.py` carrega as variáveis de ambiente.
2. `SupabaseContatoRepository` busca contatos na tabela `contatos`.
3. `build_message()` monta a mensagem personalizada.
4. `DisparaAiClient` envia um `POST` JSON para o webhook da Dispara.ai.
5. O gatilho da Dispara.ai recebe o payload e inicia o fluxo configurado.
6. O fluxo usa o campo mapeado, como `mensagem_python`, para enviar a mensagem pelo WhatsApp.

## Solução de problemas

- **Recebe `204`, mas não chega mensagem no WhatsApp:** o webhook chegou na Dispara.ai, mas o fluxo, canal ou mapeamento precisa ser revisado.
- **Chega `@text` ou `@mensagem_python` literalmente:** a variável foi digitada como texto; selecione o campo pelo menu de variáveis da Dispara.ai.
- **Mensagem fixa chega, mas variável não chega:** revise o mapeamento do gatilho, principalmente `body.mensagem_python` para o campo personalizado `mensagem_python`.
- **Erro de canal desconectado:** conecte o WhatsApp e vincule o canal ao fluxo/gatilho na Dispara.ai.

Referência Dispara.ai: [Integração com GoogleForms](https://ajudadispara.crisp.help/pt-br/article/integracao-com-o-googleforms-1sicagu/)

## Licença

MIT
