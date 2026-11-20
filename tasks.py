
from database import get_connection

STATUSES = ["Pendente", "Em andamento", "Concluída"]
PRIORITIES = ["Baixa", "Média", "Alta"]


def validate_task(title, status, priority):
    if not title or not title.strip():
        raise ValueError("O título da tarefa é obrigatório.")

    if status not in STATUSES:
        raise ValueError("Status inválido.")

    if priority not in PRIORITIES:
        raise ValueError("Prioridade inválida.")


def create_task(title, description="", priority="Média",
                due_date=None, status="Pendente", db_path=None):

    validate_task(title, status, priority)

    with get_connection(db_path) as connection:
        cursor = connection.execute("""
            INSERT INTO tasks (title, description, priority, due_date, status)
            VALUES (?, ?, ?, ?, ?)
        """, (title.strip(), description, priority, due_date, status))

        return cursor.lastrowid


def get_tasks(status=None, priority=None, search=None, db_path=None):
    query = "SELECT * FROM tasks WHERE 1=1"
    params = []

    if status and status != "Todos":
        query += " AND status = ?"
        params.append(status)

    if priority and priority != "Todas":
        query += " AND priority = ?"
        params.append(priority)

    if search:
        query += " AND (title LIKE ? OR description LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%"])

    query += """
        ORDER BY
            CASE priority
                WHEN 'Alta' THEN 1
                WHEN 'Média' THEN 2
                WHEN 'Baixa' THEN 3
            END,
            id DESC
    """

    with get_connection(db_path) as connection:
        rows = connection.execute(query, params).fetchall()
        return [dict(row) for row in rows]


def get_task(task_id, db_path=None):
    with get_connection(db_path) as connection:
        row = connection.execute(
            "SELECT * FROM tasks WHERE id = ?",
            (task_id,)
        ).fetchone()

        return dict(row) if row else None


def update_task(task_id, title, description, priority,
                due_date, status, db_path=None):

    validate_task(title, status, priority)

    with get_connection(db_path) as connection:
        cursor = connection.execute("""
            UPDATE tasks
            SET title = ?,
                description = ?,
                priority = ?,
                due_date = ?,
                status = ?
            WHERE id = ?
        """, (title.strip(), description, priority,
              due_date, status, task_id))

        return cursor.rowcount > 0


def delete_task(task_id, db_path=None):
    with get_connection(db_path) as connection:
        cursor = connection.execute(
            "DELETE FROM tasks WHERE id = ?",
            (task_id,)
        )

        return cursor.rowcount > 0


def get_dashboard_stats(db_path=None):
    with get_connection(db_path) as connection:
        row = connection.execute("""
            SELECT
                COUNT(*) AS total,
                SUM(CASE WHEN status = 'Pendente' THEN 1 ELSE 0 END) AS pending,
                SUM(CASE WHEN status = 'Em andamento' THEN 1 ELSE 0 END) AS in_progress,
                SUM(CASE WHEN status = 'Concluída' THEN 1 ELSE 0 END) AS completed,
                SUM(
                    CASE
                        WHEN due_date IS NOT NULL
                        AND due_date < date('now', 'localtime')
                        AND status != 'Concluída'
                        THEN 1 ELSE 0
                    END
                ) AS overdue
            FROM tasks
        """).fetchone()

        return dict(row)
