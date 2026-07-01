# Backend — Sistema de Gestión de Urgencias y Triaje

Monolito modular + hexagonal (Python + FastAPI + SQLAlchemy + PostgreSQL).
Un módulo por carpeta bajo `app/modules/`, cada uno con
`domain/ · application/ · infrastructure/ · api/`.

## Arrancar en local

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt

docker compose up -d          # Postgres en localhost:55432
alembic upgrade head           # crea/actualiza el esquema

uvicorn app.main:app --reload
```

## Tests

Requieren Postgres real (no mocks) — crear una base separada para
tests una sola vez:

```bash
docker exec <contenedor_postgres> psql -U posta -d posta_urgencias -c "CREATE DATABASE posta_test;"
DATABASE_URL="postgresql+psycopg://posta:posta@localhost:55432/posta_test" alembic upgrade head

pytest --cov=app.modules --cov-branch
```

Cada test de infraestructura corre dentro de un SAVEPOINT que se
revierte al terminar — no hay fixtures fijos, los datos son reales
por corrida.

## Módulos construidos

- `registro_pacientes`
- `triaje`

Los otros 5 módulos del proyecto están bloqueados por falta de
fase-0 congelada — ver `.orquestador/ledger-dependencias.md`.
