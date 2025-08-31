# HH Parser — Парсер вакансий с hh.ru

## Описание проекта
Проект создан для поиска вакансий с сайта [hh.ru](https://hh.ru) за текущий день.  
Позволяет фильтровать вакансии по ключевым словам, опыту, занятости и графику, а также сохранять результат в JSON, TXT.

---

## Структура проекта
- **data/**: Директория для хранения данных (например, JSON-файлов) и временных файлов.  
- **htmlcov/**: Отчёты покрытия тестов (coverage).  
- **src/app/**  
  - `vacancy_parser_app.py`: Основной класс приложения `VacancyParserApp`.  
- **src/models/**  
  - `vacancy.py`: Класс `Vacancy` с атрибутами и методами для работы с вакансиями.  
  - `abstracts.py`: Абстрактные классы для saver-ов (`BaseSaverVacancy`).  
- **src/services/**  
  - `head_hunter_api.py`: Работа с API HeadHunter для получения вакансий.  
  - `savers.py`: Классы `JSONSaver` и `TXTSaver` для сохранения вакансий.  
  - `vacancy_selector.py`: Класс `VacancySelector` для фильтрации и сортировки вакансий.  
- **src/config.py**: Конфигурационные параметры проекта.  
- **src/main.py**: Точка входа в приложение.  
- **src/menus.py**: Консольные меню и обработка пользовательского ввода.  
- **tests/**: Папка с тестами для проверки работы классов и функций.  
  - `conftest.py`: Фикстуры для тестов.  
  - `test_head_hunter_api.py`: Тесты API HeadHunter.  
  - `test_savers.py`: Тесты `JSONSaver` и `TXTSaver`.  
  - `test_vacancy.py`: Тесты класса `Vacancy`.  
  - `test_vacancy_parser_app.py`: Тесты `VacancyParserApp`.  
  - `test_vacancy_selector.py`: Тесты `VacancySelector`.
- `.flake8`: Конфигурация линтера Flake8.  
- `.gitignore`: Игнорируемые Git файлы.

---

## Установка
##### Для пользователя:
1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/Andrew-Krygin/Vacparser.git
   ```
   
2. Перейдите в каталог проекта:
   ```bash
   cd Vacparser
   ```
   
3. Установите зависимости с помощью Poetry:
   ```bash
   poetry install
   ```
   

##### Для разработчика:
1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/Andrew-Krygin/Vacparser.git
   ```
   
2. Перейдите в каталог проекта:
   ```bash
   cd Vacparser
   ```
   
3. Установите зависимости с помощью Poetry:
   ```bash
   poetry install
   ```
   
---

## Примеры использования
Будут добавлены позднее.

---

## Тестирование
Проект использует pytest для модульного тестирования и pytest-cov для оценки покрытия кода. 

- Установите необходимые зависимости для разработки:
   ```bash
   poetry add --dev pytest pytest-cov
   ```

### Запуск тестов
- Для запуска всех тестов:
   ```bash
   poetry run pytest
   ```

- Для более подробного вывода:
   ```bash
   poetry run pytest -v
   ```
  
---

### Проверка покрытия кода
- Запуск с отображением процента покрытия:
   ```bash
   poetry run pytest --cov=src
   ```

- Для генерации HTML-отчёта покрытия:
   ```bash
   poetry run pytest --cov=src --cov-report=html
   ```

HTML-отчёт будет доступен по пути `htmlcov/index.html`.

---

### Структура тестов
- Все тесты расположены в директории `tests/`.
- Покрываются модули `src/app`, `models/vacancy`, `services/head_hunter_api`, `services/savers`, 
  `services/vacancy_selector`.
---

## Авторы
- [Andrew Krygin](https://github.com/Andrew-Krygin)
