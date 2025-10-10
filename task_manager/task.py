from enum import IntEnum, Enum
from datetime import datetime

class Priority(IntEnum):
    BAIXA = 1
    MEDIA = 2
    ALTA = 3

class Status(Enum):
    PENDENTE = "Pendente"
    EM_ANDAMENTO = "Em Andamento"
    CONCLUIDA = "Concluída"

class Task:
    def __init__(self, id: int = None, titulo: str = "", descricao: str = "", prioridade: Priority = Priority.BAIXA, prazo: datetime = None, status: Status = Status.PENDENTE):
        self.id = id
        self.titulo = titulo
        self.descricao = descricao
        self.prioridade = prioridade
        self.prazo = prazo
        self.status = status

    def validar(self):
        if not self.titulo or len(self.titulo) < 3:
            raise ValueError("O título da tarefa deve ter pelo menos 3 caracteres.")
        if self.prazo < datetime.now():
            raise ValueError("O prazo da tarefa não pode ser no passado.")