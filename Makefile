SRCDIRS=./tests/ ./emendis/

start:
	uvicorn emendis.main:app --reload

test:
	pytest -svv --pdb

load-data:
	./cli.py load-csv ./data\[97\].csv

format:
	isort $(SRCDIRS)
	black $(SRCDIRS)
	pflake8 $(SRCDIRS)

