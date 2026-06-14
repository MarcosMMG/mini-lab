# Arquitetura do Controle de Atendimentos
Este projeto possui uma arquitetura simples de aplicação web full stack,
especializada para o domínio de Atendimento e orientada a eventos (Etapa 3).

## Domínio
Atendimento ao cliente. As demandas representam atendimentos, classificados em
Suporte, Reclamação e Solicitação. Eventos externos (formulário web, chat,
etc.) geram demandas automaticamente.

## Frontend
O frontend foi construído com HTML, CSS e JavaScript puro.
Ele exibe o formulário de cadastro, a lista de demandas, o painel resumo e a
seção de eventos recebidos. As funções `fetchEvents()` e `renderEvents()`
carregam e exibem os eventos junto com as demandas e o resumo.

## Backend
O backend foi construído com FastAPI.
Ele oferece rotas para listar, criar, atualizar, excluir demandas e gerar
resumo, além das rotas orientadas a eventos:
- `POST /event` — registra o evento e gera uma demanda automaticamente.
- `GET /events` — lista os eventos recebidos.

A função `convert_event_to_demand()` em `services.py` transforma um evento em
uma demanda, mapeando o tipo do evento para a categoria do domínio.

## Fluxo de eventos
```
Evento → API (POST /event) → Backend (registra evento + converte em demanda)
       → Banco (events + demands) → Frontend (exibe eventos e demandas)
```

## Banco de dados
O banco utilizado é SQLite.
Ele armazena duas tabelas:
- `demands` — demandas cadastradas (manuais ou geradas por eventos).
- `events` — eventos externos recebidos (source, type, value, created_at).

## Infraestrutura
O sistema roda localmente com Docker e Docker Compose.
Isso permite que o ambiente funcione de forma reproduzível.

## Papel da IA
A IA pode ser usada como apoio para explicar, revisar e comparar soluções.
Nesta etapa, a referência principal é o gabarito oficial do projeto.
