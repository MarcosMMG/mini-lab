from pathlib import Path
import sqlite3

DB_PATH = Path("/data/lab.db")


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS demands (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT NOT NULL,
                status TEXT NOT NULL,
                owner TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        count = connection.execute("SELECT COUNT(*) FROM demands").fetchone()[0]
        if count == 0:
            connection.executemany(
                """
                INSERT INTO demands (title, category, description, status, owner, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                [
                    (
                        "Organizar evento comunitario",
                        "Comunidade",
                        "Planejar local, divulgacao e equipe de apoio",
                        "pendente",
                        "Marina",
                        "2026-04-11",
                    ),
                    (
                        "Cadastrar voluntarios",
                        "ONG",
                        "Registrar nome, contato e area de interesse",
                        "em andamento",
                        "Carlos",
                        "2026-04-11",
                    ),
                    (
                        "Atualizar agenda escolar",
                        "Educacao",
                        "Publicar calendario com atividades do mes",
                        "concluída",
                        "Luciana",
                        "2026-04-11",
                    ),
                ],
            )
            connection.commit()


def list_demands():
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT id, title, category, description, status, owner, created_at
            FROM demands
            ORDER BY id
            """
        ).fetchall()
    return [dict(row) for row in rows]


def get_demand_by_id(demand_id: int):
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT id, title, category, description, status, owner, created_at
            FROM demands
            WHERE id = ?
            """,
            (demand_id,),
        ).fetchone()
    return dict(row) if row else None


def create_demand(title, category, description, status, owner, created_at):
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO demands (title, category, description, status, owner, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (title, category, description, status, owner, created_at),
        )
        connection.commit()
    return get_demand_by_id(cursor.lastrowid)


def update_demand(demand_id, title, category, description, status, owner, created_at):
    with get_connection() as connection:
        connection.execute(
            """
            UPDATE demands
            SET title = ?, category = ?, description = ?, status = ?, owner = ?, created_at = ?
            WHERE id = ?
            """,
            (title, category, description, status, owner, created_at, demand_id),
        )
        connection.commit()
    return get_demand_by_id(demand_id)


def delete_demand(demand_id):
    with get_connection() as connection:
        connection.execute(
            "DELETE FROM demands WHERE id = ?",
            (demand_id,),
        )
        connection.commit()


def get_summary():
    with get_connection() as connection:
        total = connection.execute("SELECT COUNT(*) FROM demands").fetchone()[0]
        pending = connection.execute(
            "SELECT COUNT(*) FROM demands WHERE status = 'pendente'"
        ).fetchone()[0]
        in_progress = connection.execute(
            "SELECT COUNT(*) FROM demands WHERE status = 'em andamento'"
        ).fetchone()[0]
        done = connection.execute(
            "SELECT COUNT(*) FROM demands WHERE status = 'concluída'"
        ).fetchone()[0]
    return {
        "total": total,
        "pending": pending,
        "in_progress": in_progress,
        "done": done,
    }
