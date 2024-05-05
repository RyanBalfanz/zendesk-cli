.PHONY: all
all:

.PHONY: clean
clean:
	ruff clean
	pyclean .

.PHONY: test
test:
	pytest

.PHONY: housekeeping
housekeeping: checkmake fmt lint

fmt:
	ruff format .
	isort .

lint:
	ruff check .

checkmake:
	checkmake Makefile
