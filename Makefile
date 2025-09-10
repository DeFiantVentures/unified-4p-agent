.PHONY: install run test example
install:
	pip install -r requirements.txt
run:
	uvicorn server.app:app --host 0.0.0.0 --port 8000
test:
	pytest -q
example:
	python examples/run_example.py
