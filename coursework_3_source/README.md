# Исходный код для курсовой работы №3

## Описание проекта
- Установка зависимостей
```shell
pip install -r requirements.txt

pip install -r coursework_3_source/requirements.dev.txt
pip install -r requirements.dev.txt
```

- Создание моделей (очистит БД и создаст все модели, указанные в импорте)
```shell
python coursework_3_source/create_tables.py
```

- Загрузка данных в базу
```shell
python load_fixture.py
```
Скрпит читает файл fixtures.json и загружает данные в базу. Если данные уже загружены - выводит соответсвующее сообщение. 

## Запуск проекта

### Bash (Linux/MACOS)
```shell
export FLASK_APP=run.py
export FLASK_ENV='development'
flask run
```

### CMD (Windows)
```shell
set FLASK_APP=run.py
set FLASK_ENV=development
flask run
```

### PowerShell (Windows)
```shell
$env:FLASK_APP = "run"
$env:FLASK_ENV = "development"
flask run
```

## Запуск тестов
```shell
pytest .
```

