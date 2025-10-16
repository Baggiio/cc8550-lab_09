from datetime import datetime, timedelta

from task_manager.repository import TaskRepository
from task_manager.service import TaskService
from task_manager.task import Priority, Status, Task
from task_manager.storage import InMemoryStorage


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


def test_save_funciona_com_subclasse_de_storage():
    class StoragePersonalizado(InMemoryStorage):
        def __init__(self):
            super().__init__()
            self.registros_add = []

        def add(self, id, item):
            self.registros_add.append((id, item))
            super().add(id, item)

    storage = StoragePersonalizado()
    repo = TaskRepository(storage)
    task = Task(None, "Generica", "Descricao", Priority.MEDIA, datetime.now() + timedelta(days=1))

    resultado = repo.save(task)

    assert storage.registros_add == [(1, resultado)]
    assert storage.get(1) is resultado


def test_task_service_component_flow():
    storage = InMemoryStorage()
    repository = TaskRepository(storage)
    service = TaskService(repository)
    prazo = datetime.now() + timedelta(days=3)

    criada = service.criar_tarefa("Integra", "Fluxo completo", Priority.ALTA, prazo)
    tarefas = list(service.listar_todas())
    atualizada = service.atualizar_status(criada.id, Status.CONCLUIDA)

    assert criada.id == 1
    assert storage.get(criada.id) is criada
    assert len(tarefas) == 1 and tarefas[0] is criada
    assert atualizada.status is Status.CONCLUIDA
