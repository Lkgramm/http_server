# Makefile
.PHONY: server test loadtest lint format check install clean

# Цвета и вывод отключены для Windows
GREEN =
YELLOW =
RESET =

# Команды
SERVER = run_server.py
TEST_DIR = tests
FUNCTIONAL_TEST = $(TEST_DIR)/functional/test_functional.py
LOAD_TEST = $(TEST_DIR)/load/test_load.py

# Вывод help по командам
help:
	@echo Доступные команды:
	@echo   make server			— Запустить HTTP-сервер
	@echo   make test			— Запустить функциональные тесты
	@echo   make loadtest		— Запустить нагрузочное тестирование
	@echo   make lint			— Проверить стиль кода с помощью flake8
	@echo   make format			— Отформатировать код с помощью black
	@echo   make check			— Проверить стиль + формат
	@echo   make install		— Установить зависимости через Poetry
	@echo   make clean			— Очистить __pycache__ и .pyc файлы

# Запуск сервера
server:
	@echo run server...
	poetry run python run_server.py

# Функциональные тесты
test:
	@echo run functional test...
	poetry run pytest $(FUNCTIONAL_TEST)

# Нагрузочное тестирование
loadtest:
	@echo run laod test...
	poetry run locust -f tests/load/test_load.py --host=http://127.0.0.1:8000

# Проверка стиля кода
lint:
	@echo check code style with flake8...
	poetry run flake8 server/ tests/ scripts/ --ignore=E501

# Форматирование кода
format:
	@echo format code with black...
	poetry run black server/ tests/ scripts/

# Проверка форматирования и стиля
check: format lint

# Установка зависимостей
install:
	@echo install dependencies via Poetry...
	poetry install
