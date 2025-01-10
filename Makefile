.PHONY: check
check:
	uvx ruff check src . --fix
	uvx ruff format src .
	uvx pyright
