.PHONY: check
check:
	poetry run ruff check . --fix
	poetry run ruff format .
