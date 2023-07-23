lint:
	poetry run isort pyeo tests
	poetry run flake8 pyeo
	poetry run mypy pyeo

test:
	poetry run pytest
