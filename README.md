# cc8550-lab_09

## Passo a passo para configurar o ambiente Python

1. Crie um ambiente virtual:
    ```bash
    python3 -m venv venv
    ```

2. Ative o ambiente virtual:
    ```bash
    source venv/bin/activate
    ```

3. Instale as dependências do `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

## Como rodar os testes

Para executar os testes, utilize os seguintes comandos:

```bash
python -m pytest -v
```

Para verificar a cobertura dos testes:

```bash
python -m pytest --cov=task_manager/
```