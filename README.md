# 📊 Log Analyzer

CLI-приложение для анализа логов Django-приложений и генерации отчётов.

---

## 🧾 Что делает проект

- Принимает один или несколько лог-файлов
- Фильтрует только `django.request`
- Считает количество запросов к API по каждому уровню логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Формирует табличный отчёт в консоль
- Готов к расширению под новые виды отчётов

---

## 📦 Требования

-  Python 3.10+
- Стандартная библиотека
- Для тестов: pytest, pytest-cov

---

## 🛠 Как запустить

### 1. Установить зависимости (если нужно)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

⚠️ Используется только стандартная библиотека, кроме pytest и pytest-cov для тестов !
```
### 2. Запустить анализ логов
```bash
python main.py logs/app1.log logs/app2.log logs/app3.log --report handlers
```

###  📊 Пример вывода:
```bash
Total requests: 188

HANDLER                  DEBUG     INFO      WARNING   ERROR     CRITICAL  
/admin/dashboard/        0         13        0         4         0         
/admin/login/            0         12        0         4         0         
/api/v1/auth/login/      0         12        0         2         0         
/api/v1/orders/          0         10        0         4         0         
/api/v1/support/         0         16        0         4         0         
... (и т.д.)
```

---

## 🧩 Как добавить новый отчёт

#### 1. Создать файл в reports/, например reports/errors.py
#### 2. Добавить туда функцию:
```python
def generate_report(data: Dict[str, Dict[str, int]]) -> None:
    # ваша логика
```
#### 3. Зарегистрировать отчёт в main.py:
```python
from reports.errors import generate_report as errors_report

AVAILABLE_REPORTS = {
    "handlers": generate_report,
    "errors": errors_report
}
```

---

## ✅ Проверки и тесты

### Протестированы:
- Парсинг строк django.request
- Чтение лог-файлов
- Вывод итогового отчёта
- Покрытие тестами: 98%

### Запуск тестов:
```bash
python -m pytest
```
### Запуск с покрытием:
```bash
python -m pytest --cov=parser --cov=reports
```

###  📊 Пример вывода:
```bash
========================================================================================== test session starts ==========================================================================================
platform darwin -- Python 3.12.6, pytest-8.3.5, pluggy-1.5.0
rootdir: /Users/sherzodrts/PycharmProjects/log-analyzer
plugins: cov-6.1.1
collected 5 items                                                                                                                                                                                       

tests/test_parser.py ....                                                                                                                                                                         [ 80%]
tests/test_reports.py .                                                                                                                                                                           [100%]

============================================================================================ tests coverage =============================================================================================
___________________________________________________________________________ coverage: platform darwin, python 3.12.6-final-0 ____________________________________________________________________________

Name                   Stmts   Miss  Cover
------------------------------------------
parser/__init__.py         0      0   100%
parser/log_parser.py      24      1    96%
reports/__init__.py        0      0   100%
reports/handlers.py       19      0   100%
------------------------------------------
TOTAL                     43      1    98%
=========================================================================================== 5 passed in 0.03s ===========================================================================================
```

---

## 📁 Структура проекта
```perl
log-analyzer/
├── logs/                   # Примеры логов
├── parser/                 # Парсинг логов
│   └── log_parser.py
├── reports/                # Отчёты
│   └── handlers.py
├── tests/                  # Pytest-тесты
│   └── test_parser.py
├── main.py                 # Точка входа
├── README.md
└── requirements.txt        # (если используешь)
```




