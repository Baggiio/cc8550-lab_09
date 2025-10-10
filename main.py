from datetime import datetime, timedelta
from task_manager.task import Task, Priority
from task_manager.storage import InMemoryStorage
from task_manager.repository import TaskRepository

# Criar componentes
storage = InMemoryStorage()
repo = TaskRepository(storage)

# Criar tarefa
prazo = datetime.now() + timedelta(days=5)
task = Task(None, "Estudar", "Python", Priority.ALTA, prazo)
task.validar()

# Salvar
task_salva = repo.save(task)
print(f"ID: {task_salva.id}")

# Buscar
encontrada = repo.find_by_id(1)
print(f"Titulo: {encontrada.titulo}")