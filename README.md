# Mini AI-Native Dev Lab
## Objetivo
Laboratório local full stack com frontend, backend, API, banco e uso inicial
de agente de IA no editor.
## Como executar
docker compose up --build
## Endereços
Frontend: http://localhost:8080
API: http://localhost:8000/projects
Docs da API: http://localhost:8000/docs

# Controle de Atendimentos
## Objetivo

Sistema da disciplina Projeto de Extensão em Software Full Stack, especializado
para o domínio de **Atendimento** (Etapa 3). Além do cadastro manual de
demandas, o sistema é orientado a eventos: recebe eventos externos e os
transforma automaticamente em demandas de atendimento.

## Domínio escolhido
Atendimento ao cliente. As demandas representam atendimentos e são organizadas
nas categorias **Suporte**, **Reclamação** e **Solicitação**.

## Funcionalidades
- cadastrar demandas manualmente
- listar demandas
- excluir demandas
- exibir resumo por status
- receber eventos externos (`POST /event`)
- transformar eventos em demandas automaticamente
- registrar e listar eventos recebidos (`GET /events`)
- exibir eventos e demandas no frontend

## Fluxo de eventos
```
Evento → POST /event → registra na tabela events
                     → convert_event_to_demand() gera a demanda
                     → salva a demanda → retorna sucesso
Frontend → "Carregar dados" → exibe demandas, resumo e eventos
```

### Exemplo de evento (domínio Atendimento)
```json
{
  "source": "formulario-web",
  "type": "solicitacao",
  "value": "segunda via de boleto",
  "created_at": "2026-06-01"
}
```
O tipo do evento é mapeado para a categoria da demanda
(`solicitacao` → Solicitação, `reclamacao` → Reclamação, `duvida` → Suporte).

## Tecnologias
- FastAPI
- SQLite
- HTML
- CSS
- JavaScript
- Docker
- Docker Compose
- Git

## Endpoints principais
- `GET /health` — status da API
- `GET /demands` — lista demandas
- `POST /demands` — cria demanda manual
- `PUT /demands/{id}` — atualiza demanda
- `DELETE /demands/{id}` — remove demanda
- `GET /summary` — resumo por status
- `POST /event` — recebe evento e gera demanda
- `GET /events` — lista eventos recebidos

## Como executar
docker compose up --build
