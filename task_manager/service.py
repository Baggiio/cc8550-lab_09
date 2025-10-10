from datetime import datetime
from typing import Iterable

from task_manager.repository import TaskRepository
from task_manager.task import Priority, Status, Task


class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def criar_tarefa(
        self,
        titulo: str,
        descricao: str,
        prioridade: Priority,
        prazo: datetime,
        status: Status = Status.PENDENTE,
    ) -> Task:
        task = Task(None, titulo, descricao, prioridade, prazo, status)
        task.validar()
        return self.repository.save(task)

    def listar_todas(self) -> Iterable[Task]:
        return self.repository.find_all()

    def atualizar_status(self, id: int, status: Status) -> Task:
        task = self.repository.find_by_id(id)
        if task is None:
            raise ValueError(f"Tarefa com id {id} não encontrada.")
        task.status = status
        return task
