#!/bin/sh

poetry run alembic upgrade head

poetry run uvicorn --host 0.0.0.0 --port 8000 gb_cashback.app:app