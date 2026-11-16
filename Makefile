# Run the evalguard example with the same inputs documented in the quickstart.
.PHONY: dev test lint

dev:
	python evalguard.py examples/evalguard.json

test:
	python -m pytest --cov=evalguard --cov-fail-under=70

lint:
	ruff check .
	ruff format --check .
	mypy evalguard.py
