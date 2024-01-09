pretty:
	isort defillama/ && isort tests/
	black defillama/ && black tests/

test:
	pytest tests/ -vv -ss
cov:
	coverage run --source=defillama -m pytest tests/ -vv -ss && coverage report -m