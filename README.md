# Travel Assistant

## Installation

Install poetry

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Verify that Poetry is correctly installed:

```bash
poetry --version
```

## Install dependencies

```bash
poetry install
```

## Run script

```bash
poetry run python main.py
```

## Create request

```bash
curl -X POST "http://localhost:8100/chat/" -H "Content-Type: application/json" -d '{"content": "Hola, necesito un hotel en Santiago para 1 noche a partir del 4 de noviembre de este año 2024, para mi esposa, mi hijo de 3 años y yo."}'
```