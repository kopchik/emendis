SRCDIRS=./tests/ ./emendis/

install:
	pip install -r requirements.txt
	pip install -e .

start:
	uvicorn emendis.main:app --reload

test:
	pytest -svv --pdb

load-csv:
	emendis load-csv tests/test_data.csv

clean:
	rm -rf .direnv || true
	rm *.sqlite || true
	find ./ -name __pycache__ -exec rm -rf {} \; || true

format:
	isort $(SRCDIRS)
	black $(SRCDIRS)
	pflake8 $(SRCDIRS)
	poetry export --with dev -f requirements.txt --output requirements.txt
