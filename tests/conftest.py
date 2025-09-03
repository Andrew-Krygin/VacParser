import pathlib

import pytest

from src.app.vacancy_parser_app import VacancyParserApp
from src.models.vacancy import Vacancy
from src.services.savers import JSONSaver, TXTSaver
from src.services.vacancy_selector import VacancySelector


@pytest.fixture
def sample_vacancy_1() -> Vacancy:
    """Возвращает пример вакансии 'Автомойщик' с заполненными полями для тестирования."""
    return Vacancy(
        "122377605",
        "Автомойщик",
        "https://hh.ru/vacancy/122377605",
        100000,
        150000,
        "Опыт работы на автомойке.",
        "Профессиональная мойка кузова, дисков.",
    )


@pytest.fixture
def sample_empty_vacancy_1() -> Vacancy:
    """Возвращает пустую вакансию для тестирования обработки отсутствующих данных."""
    return Vacancy(
        "",
        "",
        "",
        "",  # type: ignore
        "",  # type: ignore
        "",
        "",
    )


@pytest.fixture
def sample_vacancy_2() -> Vacancy:
    """Возвращает пример вакансии 'Водитель-экспедитор' с заполненными полями для тестирования."""
    return Vacancy(
        "122497603",
        "Водитель-экспедитор кат. 'В' на авто Форд, Ивеко (будки)",
        "https://hh.ru/vacancy/122497603",
        56000,
        180000,
        "Наличие ИП. Опыт работы в сфере транспортно-экспедиторских услуг.",
        "Выгрузка автомобиля (2-3 тонны) - силами водителя!",
    )


@pytest.fixture
def sample_json_saver() -> JSONSaver:
    """Создает экземпляр JSONSaver для тестирования сохранения вакансий в формате JSON."""
    return JSONSaver()


@pytest.fixture
def sample_vacancies() -> list[Vacancy]:
    """Возвращает список из нескольких вакансий для тестирования фильтров и селектора вакансий."""
    return [
        Vacancy(
            id_vacancy="1",
            name_vacancy="Python Developer",
            url="https://example.com/job/1",
            salary_from=80000,
            salary_to=120000,
            skills="Python, Django",
            responsibilities="Develop, Maintain",
        ),
        Vacancy(
            id_vacancy="2",
            name_vacancy="Java Developer",
            url="https://example.com/job/2",
            salary_from=90000,
            salary_to=130000,
            skills="Java, Spring",
            responsibilities="Develop, Test",
        ),
        Vacancy(
            id_vacancy="3",
            name_vacancy="Front-End Developer",
            url="https://example.com/job/3",
            salary_from=70000,
            salary_to=100000,
            skills="JavaScript, React",
            responsibilities="Develop UI",
        ),
        Vacancy(
            id_vacancy="4",
            name_vacancy="Data Scientist",
            url="https://example.com/job/4",
            salary_from=95000,
            salary_to=140000,
            skills="Python, ML",
            responsibilities="Analyze data",
        ),
        Vacancy(
            id_vacancy="5",
            name_vacancy="Web Developer",
            url="https://example.com/job/5",
            salary_from=60000,
            salary_to=80000,
            skills="HTML, CSS",
            responsibilities="Create websites",
        ),
    ]


@pytest.fixture
def sample_selector(sample_vacancies: list[Vacancy]) -> VacancySelector:
    """Фикстура для создания экземпляра VacancySelector"""
    return VacancySelector(sample_vacancies)


class DummySaver:
    """Имитация класса Saver для тестирования VacancyParserApp без записи в файлы."""

    def __init__(self) -> None:
        self.vacancies: list[Vacancy] = []
        self.saved = False
        self.added = False
        self.removed_id: str | None = None

    def write_vacancies(self, vacancies: list) -> None:
        self.vacancies.extend(vacancies)
        self.saved = True

    def add_vacancy(self, vacancy: Vacancy) -> None:
        self.vacancies.append(vacancy)
        self.added = True

    def remove_vacancies(self, vacancy_id: str) -> None:
        self.removed_id = vacancy_id
        self.vacancies = [v for v in self.vacancies if getattr(v, "id", None) != vacancy_id]


@pytest.fixture
def dummy_savers() -> dict:
    """Возвращает словарь с двумя DummySaver для тестирования интерфейса сохранения."""
    return {"1": DummySaver(), "2": DummySaver()}


@pytest.fixture
def app(dummy_savers: dict) -> VacancyParserApp:
    """Создает экземпляр VacancyParserApp с подменными saver-ами для тестирования."""
    return VacancyParserApp(api=None, savers=dummy_savers)


@pytest.fixture
def txt_saver(tmp_path: pathlib.Path) -> TXTSaver:
    """Создает экземпляр TXTSaver с временным файлом для безопасного тестирования записи в txt."""
    file_path = tmp_path / "vacancies.txt"
    return TXTSaver(filename=str(file_path))
