from app.database import get_summary, list_demands


def normalize_status(status: str) -> str:
    value = status.strip().lower()
    valid_status = ["pendente", "em andamento", "concluída"]
    if value not in valid_status:
        return "pendente"
    return value


def build_summary():
    return get_summary()


def list_all_demands():
    return list_demands()


def convert_event_to_demand(event: dict) -> dict:
    """Transforma um evento externo em uma demanda de atendimento."""
    source = event["source"]
    event_type = event["type"]
    value = event["value"]
    created_at = event["created_at"]
    return {
        "title": f"Atendimento gerado por evento: {event_type}",
        "category": normalize_status_category(event_type),
        "description": f"Evento recebido de {source}: {value}",
        "status": "pendente",
        "owner": source,
        "created_at": created_at,
    }


def normalize_status_category(event_type: str) -> str:
    """Mapeia o tipo de evento para uma categoria do domínio de atendimento."""
    mapping = {
        "solicitacao": "Solicitação",
        "solicitação": "Solicitação",
        "reclamacao": "Reclamação",
        "reclamação": "Reclamação",
        "duvida": "Suporte",
        "dúvida": "Suporte",
        "suporte": "Suporte",
    }
    return mapping.get(event_type.strip().lower(), "Solicitação")
