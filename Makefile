pretty:
	isort dfllama/ && isort tests/
	black dfllama/ && black tests/

test:
	pytest tests/ -vv -ss
cov:
	coverage run --source=dfllama -m pytest tests/ -vv -ss && coverage report -m