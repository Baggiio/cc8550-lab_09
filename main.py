from datetime import datetime

from task_manager.repository import TaskRepository
from task_manager.service import TaskService
from task_manager.storage import InMemoryStorage
from task_manager.task import Priority, Status


def exibir_menu() -> str:
    print("\n=== Task Manager ===")
    print("1 - Criar tarefa")
    print("2 - Listar tarefas")
    print("3 - Atualizar status")
    print("4 - Sair")
    return input("Escolha uma opção: ").strip()


def selecionar_prioridade() -> Priority:
    for prioridade in Priority:
        print(f"{prioridade.value} - {prioridade.name.title()}")
    valor = int(input("Escolha a prioridade: ").strip())
    return Priority(valor)


def selecionar_status() -> Status:
    for idx, status in enumerate(Status, start=1):
        print(f"{idx} - {status.value}")
    valor = int(input("Escolha o novo status: ").strip())
    return list(Status)[valor - 1]


def obter_prazo() -> datetime:
    texto = input("Informe o prazo (YYYY-MM-DD): ").strip()
    return datetime.strptime(texto, "%Y-%m-%d")


def criar_tarefa(service: TaskService) -> None:
    titulo = input("Título: ").strip()
    descricao = input("Descrição: ").strip()
    prioridade = selecionar_prioridade()
    prazo = obter_prazo()
    try:
        tarefa = service.criar_tarefa(titulo, descricao, prioridade, prazo)
        print(f"Tarefa criada com ID {tarefa.id}")
    except ValueError as erro:
        print(f"Erro ao criar tarefa: {erro}")


def listar_tarefas(service: TaskService) -> None:
    tarefas = service.listar_todas()
    if not tarefas:
        print("Nenhuma tarefa cadastrada.")
        return
    for tarefa in tarefas:
        prazo_formatado = tarefa.prazo.strftime("%Y-%m-%d") if tarefa.prazo else "Sem prazo"
        print(f"[{tarefa.id}] {tarefa.titulo} - {tarefa.status.value} - Prazo: {prazo_formatado}")


def atualizar_status(service: TaskService) -> None:
    try:
        id_tarefa = int(input("Informe o ID da tarefa: ").strip())
        novo_status = selecionar_status()
        tarefa = service.atualizar_status(id_tarefa, novo_status)
        print(f"Tarefa {tarefa.id} atualizada para {tarefa.status.value}.")
    except ValueError as erro:
        print(f"Erro: {erro}")


def main() -> None:
    storage = InMemoryStorage()
    repository = TaskRepository(storage)
    service = TaskService(repository)

    while True:
        opcao = exibir_menu()
        if opcao == "1":
            criar_tarefa(service)
        elif opcao == "2":
            listar_tarefas(service)
        elif opcao == "3":
            atualizar_status(service)
        elif opcao == "4":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()
