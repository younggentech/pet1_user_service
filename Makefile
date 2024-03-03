CODE_FOLDERS := src
UNIT_TEST_FOLDERS := unit_tests
FUNC_TEST_FOLDER := func_tests

.PHONY: unit_tests format lint security_checks func_tests

unit_tests:
	poetry run pytest $(TEST_FOLDER) --cov=$(CODE_FOLDERS) --ignore=${FUNC_TEST_FOLDER} --cov-fail-under=80

format:
	poetry run black --line-length 79 .

lint:
	poetry run black --line-length 79 --check $(CODE_FOLDERS) $(UNIT_TEST_FOLDERS) $(FUNC_TEST_FOLDER)
	poetry run flake8 $(CODE_FOLDERS) $(UNIT_TEST_FOLDERS) $(FUNC_TEST_FOLDER)
	poetry run ruff check $(CODE_FOLDERS) $(UNIT_TEST_FOLDERS) $(FUNC_TEST_FOLDER)

security_checks:
	poetry run bandit -r $(CODE_FOLDERS)

func_tests:
	poetry run pytest $(FUNC_TEST_FOLDER) --cov=$(CODE_FOLDERS) --ignore=${TEST_FOLDER} --cov-fail-under=80