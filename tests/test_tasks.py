
import pytest

from database import init_db
from tasks import (
    create_task,
    get_tasks,
    get_task,
    update_task,
    delete_task,
    get_dashboard_stats
)


@pytest.fixture
def db_path(tmp_path):
    path = tmp_path / "test.db"
    init_db(path)
    return path


def test_create_task(db_path):
    task_id = create_task(
        "Estudar Python",
        priority="Alta",
        db_path=db_path
    )

    task = get_task(task_id, db_path)

    assert task["title"] == "Estudar Python"
    assert task["priority"] == "Alta"


def test_create_task_without_title(db_path):
    with pytest.raises(ValueError):
        create_task("", db_path=db_path)


def test_update_task(db_path):
    task_id = create_task("Tarefa antiga", db_path=db_path)

    result = update_task(
        task_id,
        "Tarefa nova",
        "Descrição atualizada",
        "Média",
        None,
        "Em andamento",
        db_path
    )

    assert result is True
    assert get_task(task_id, db_path)["title"] == "Tarefa nova"


def test_delete_task(db_path):
    task_id = create_task("Excluir", db_path=db_path)

    assert delete_task(task_id, db_path) is True
    assert get_task(task_id, db_path) is None


def test_filter_tasks(db_path):
    create_task("Estudar Python", priority="Alta", db_path=db_path)
    create_task("Estudar SQL", priority="Baixa", db_path=db_path)

    tasks = get_tasks(priority="Alta", db_path=db_path)

    assert len(tasks) == 1
    assert tasks[0]["title"] == "Estudar Python"


def test_dashboard_stats(db_path):
    create_task("Tarefa 1", db_path=db_path)
    create_task("Tarefa 2", status="Concluída", db_path=db_path)

    stats = get_dashboard_stats(db_path)

    assert stats["total"] == 2
    assert stats["pending"] == 1
    assert stats["completed"] == 1
