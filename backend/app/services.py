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
