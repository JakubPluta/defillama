pretty:
	isort defillama/ && isort defillama/
	black defillama/ && black defillama/

test:
	pytest tests/ -vv -ss
cov:
	coverage run --source=defillama -m pytest tests/ -vv -ss && coverage report -m