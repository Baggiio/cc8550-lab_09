from datetime import datetime, timedelta

from task_manager.repository import TaskRepository
from task_manager.task import Priority, Task


def test_save_atribui_id(mocker):
    mock_storage = mocker.Mock()
    repo = TaskRepository(mock_storage)
    task = Task(None, "Teste", "Desc", Priority.BAIXA, datetime.now() + timedelta(days=1))

    resultado = repo.save(task)

    assert resultado.id == 1


def test_save_chama_storage_add(mocker):
    mock_storage = mocker.Mock()
    repo = TaskRepository(mock_storage)
    task = Task(None, "Outra", "Descricao", Priority.MEDIA, datetime.now() + timedelta(days=1))

    repo.save(task)

    mock_storage.add.assert_called_once_with(1, task)


def test_find_by_id_chama_storage_get(mocker):
    mock_storage = mocker.Mock()
    repo = TaskRepository(mock_storage)
    tarefa_esperada = Task(5, "Buscar", "Teste", Priority.ALTA, datetime.now() + timedelta(days=1))
    mock_storage.get.return_value = tarefa_esperada

    resultado = repo.find_by_id(5)

    mock_storage.get.assert_called_once_with(5)
    assert resultado is tarefa_esperada


def test_find_all_retorna_lista(mocker):
    mock_storage = mocker.Mock()
    repo = TaskRepository(mock_storage)
    tarefas = [
        Task(1, "Primeira", "Descricao A", Priority.BAIXA, datetime.now() + timedelta(days=1)),
        Task(2, "Segunda", "Descricao B", Priority.MEDIA, datetime.now() + timedelta(days=2)),
    ]
    mock_storage.get_all.return_value = tarefas

    resultado = repo.find_all()

    mock_storage.get_all.assert_called_once_with()
    assert resultado == tarefas