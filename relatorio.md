# Relatório do Laboratório 9

## Testes Implementados

### Testes Unitários

#### `tests/test_task.py`
- `test_task_valida`: confirma que uma tarefa completa com dados válidos passa na validação e mantém o título informado.
```python
def test_task_valida():
    prazo = datetime.now() + timedelta(days=1)
    task = Task(None, "Estudar", "Python", Priority.ALTA, prazo)
    task.validar()
    assert task.titulo == "Estudar"
```
- `test_titulo_curto_invalido`: garante que a validação rejeita títulos com menos de três caracteres e lança `ValueError`.
```python
def test_titulo_curto_invalido():
    prazo = datetime.now() + timedelta(days=1)
    task = Task(None, "AB", "Desc", Priority.BAIXA, prazo)
    with pytest.raises(ValueError):
        task.validar()
```

#### `tests/test_repository.py`
- `test_save_atribui_id`: assegura que o repositório atribui um identificador sequencial ao salvar uma nova tarefa.
```python
def test_save_atribui_id(mocker):
    mock_storage = mocker.Mock()
    repo = TaskRepository(mock_storage)
    task = Task(None, "Teste", "Desc", Priority.BAIXA, datetime.now() + timedelta(days=1))

    resultado = repo.save(task)

    assert resultado.id == 1
```
- `test_save_chama_storage_add`: verifica que o repositório delega ao método `add` do storage ao persistir tarefas.
```python
def test_save_chama_storage_add(mocker):
    mock_storage = mocker.Mock()
    repo = TaskRepository(mock_storage)
    task = Task(None, "Outra", "Descricao", Priority.MEDIA, datetime.now() + timedelta(days=1))

    repo.save(task)

    mock_storage.add.assert_called_once_with(1, task)
```
- `test_find_by_id_chama_storage_get`: confirma a delegação para `storage.get` e o retorno da mesma instância da tarefa.
```python
def test_find_by_id_chama_storage_get(mocker):
    mock_storage = mocker.Mock()
    repo = TaskRepository(mock_storage)
    tarefa_esperada = Task(5, "Buscar", "Teste", Priority.ALTA, datetime.now() + timedelta(days=1))
    mock_storage.get.return_value = tarefa_esperada

    resultado = repo.find_by_id(5)

    mock_storage.get.assert_called_once_with(5)
    assert resultado is tarefa_esperada
```
- `test_find_all_retorna_lista`: garante que o repositório retorna as tarefas vindas do storage ao listar todas.
```python
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
```

### Testes Orientados a Objetos e Componentes

#### `tests/test_task.py`
- `test_priority_herda_de_intenum`: valida a herança de `Priority` a partir de `IntEnum` e o comportamento numérico relativo entre prioridades.
```python
def test_priority_herda_de_intenum():
    assert issubclass(Priority, IntEnum)
    assert Priority.ALTA > Priority.BAIXA
```

#### `tests/test_repository.py`
- `test_save_funciona_com_subclasse_de_storage`: valida o polimorfismo permitindo que o repositório opere com uma subclasse de `InMemoryStorage`, registrando e persistindo tarefas corretamente.
```python
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
```
- `test_task_service_component_flow`: teste de componente (caixa branca) que exerce o fluxo completo do `TaskService`, verificando criação, listagem e atualização de status com o storage real.
```python
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
```

## TaskService
`task_manager/service.py` define `TaskService`, responsável por orquestrar a criação, listagem e atualização do status das tarefas. Ele recebe um `TaskRepository` e expõe:
- `criar_tarefa`: constrói um objeto `Task`, executa a validação e delega a persistência ao repositório.
- `listar_todas`: retorna todas as tarefas, simplesmente repassando a chamada ao repositório.
- `atualizar_status`: busca uma tarefa por ID, atualiza seu status e lança `ValueError` quando a tarefa não existe.

## main.py
O arquivo `main.py` oferece uma interface de linha de comando para testar o `TaskService` de ponta a ponta:
- Cria instâncias de `InMemoryStorage`, `TaskRepository` e `TaskService`.
- Exibe um menu simples para criar tarefas, listá-las, atualizar status ou encerrar a aplicação.
- Coleta entradas do usuário (título, descrição, prioridade, prazo e novo status) e apresenta mensagens de sucesso ou erro conforme o fluxo.

Execute via:
```bash
python main.py
```

Exemplo de sessão:
```text
=== Task Manager ===
1 - Criar tarefa
2 - Listar tarefas
3 - Atualizar status
4 - Sair
Escolha uma opção: 1
Título: Lavar o carro
Descrição: Completar antes do fim de semana
1 - Baixa
2 - Media
3 - Alta
Escolha a prioridade: 3
Informe o prazo (YYYY-MM-DD): 2024-11-30
Tarefa criada com ID 1
```

## Execução dos Testes

### `python -m pytest -v`
```text
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-8.4.2, pluggy-1.6.0 -- /home/baggio/cc8550-lab_09/venv/bin/python
cachedir: .pytest_cache
rootdir: /home/baggio/cc8550-lab_09
plugins: mock-3.15.1, cov-7.0.0
collecting ... collected 9 items

tests/test_repository.py::test_save_atribui_id PASSED                    [ 11%]
tests/test_repository.py::test_save_chama_storage_add PASSED             [ 22%]
tests/test_repository.py::test_find_by_id_chama_storage_get PASSED       [ 33%]
tests/test_repository.py::test_find_all_retorna_lista PASSED             [ 44%]
tests/test_repository.py::test_save_funciona_com_subclasse_de_storage PASSED [ 55%]
tests/test_repository.py::test_task_service_component_flow PASSED        [ 66%]
tests/test_task.py::test_task_valida PASSED                              [ 77%]
tests/test_task.py::test_titulo_curto_invalido PASSED                    [ 88%]
tests/test_task.py::test_priority_herda_de_intenum PASSED                [100%]

============================== 9 passed in 0.02s ===============================
```

### `python -m pytest --cov=task_manager/`
```text
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-8.4.2, pluggy-1.6.0
rootdir: /home/baggio/cc8550-lab_09
plugins: mock-3.15.1, cov-7.0.0
collected 9 items

tests/test_repository.py ......                                          [ 66%]
tests/test_task.py ...                                                   [100%]

================================ tests coverage ================================
_______________ coverage: platform linux, python 3.12.3-final-0 ________________

Name                         Stmts   Miss  Cover
------------------------------------------------
task_manager/__init__.py         4      0   100%
task_manager/repository.py      15      1    93%
task_manager/service.py         19      1    95%
task_manager/storage.py         16      5    69%
task_manager/task.py            23      1    96%
------------------------------------------------
TOTAL                           77      8    90%
============================== 9 passed in 0.04s ===============================
```
