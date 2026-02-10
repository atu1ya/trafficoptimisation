setup:
	python3 -m venv .venv && . .venv/bin/activate && pip install -r backend/requirements.txt pydantic-settings
	cd frontend && npm install

run:
	docker compose up --build

run-local:
	PYTHONPATH=backend uvicorn app.main:app --host 0.0.0.0 --port 8000

build-net:
	PYTHONPATH=backend python backend/scripts/build_network.py

test:
	cd backend && PYTHONPATH=. pytest
