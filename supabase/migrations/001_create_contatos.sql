-- Tabela de contatos para o desafio Supabase + Z-API
CREATE TABLE IF NOT EXISTS public.contatos (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  nome TEXT NOT NULL,
  telefone TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

ALTER TABLE public.contatos ENABLE ROW LEVEL SECURITY;

CREATE POLICY "contatos_select_anon"
  ON public.contatos
  FOR SELECT
  TO anon, authenticated
  USING (true);

-- Substitua pelos números reais (DDI + DDD + número, só dígitos)
INSERT INTO public.contatos (nome, telefone) VALUES
  ('Maria', '5511999990001'),
  ('João', '5511999990002'),
  ('Ana', '5511999990003');
