# API Gestão de Tarefas

API REST em FastAPI para gerenciamento de tarefas, com autenticação via JWT.

## Requisitos

- Python 3.12+
- pip

## Criar o ambiente virtual

```bash
python3 -m venv venv
```

## Entrar no ambiente virtual

```bash
source venv/bin/activate
```

Para sair do ambiente virtual, use:

```bash
deactivate
```

## Instalar as dependências

Com o ambiente virtual ativo:

```bash
pip install -r requirements.txt
```

## Configurar as variáveis de ambiente

Copie o arquivo de exemplo:

```bash
cp .env.example .env
```

Gere uma `SECRET_KEY` segura (usada para assinar os tokens JWT):

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Cole o valor gerado na variável `SECRET_KEY` do seu `.env`: exemplo no .env.example

```
DATABASE_URL=sqlite:///./banco.db
SECRET_KEY=cole-o-valor-gerado-aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Rodar a API

Com o ambiente virtual ativo:

```bash
uvicorn app.main:app --reload
```

A API ficará disponível em:

- Aplicação: http://127.0.0.1:8000
- Documentação (Swagger): http://127.0.0.1:8000/docs

