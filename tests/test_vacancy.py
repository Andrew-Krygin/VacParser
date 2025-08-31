from src.models.vacancy import Vacancy


class TestVacancy:
    def test_init(self, sample_vacancy_1: Vacancy) -> None:
        assert sample_vacancy_1.id_vacancy == "122377605"
        assert sample_vacancy_1.name_vacancy == "Автомойщик"
        assert sample_vacancy_1.url == "https://hh.ru/vacancy/122377605"
        assert sample_vacancy_1.salary_from == 100000
        assert sample_vacancy_1.salary_to == 150000
        assert sample_vacancy_1.skills == "Опыт работы на автомойке."
        assert sample_vacancy_1.responsibilities == "Профессиональная мойка кузова, дисков."

    def test_init_empty_vacancy(self, sample_empty_vacancy_1: Vacancy) -> None:
        assert sample_empty_vacancy_1.id_vacancy == "ID не указан"
        assert sample_empty_vacancy_1.name_vacancy == "Имя не указано"
        assert sample_empty_vacancy_1.url == "Ссылка не указана"
        assert sample_empty_vacancy_1.salary_from == 0
        assert sample_empty_vacancy_1.salary_to == 0
        assert sample_empty_vacancy_1.skills == "Нет описания"
        assert sample_empty_vacancy_1.responsibilities == "Нет описания"

    def test__str__(self, sample_vacancy_1: Vacancy) -> None:
        str_output = sample_vacancy_1.__str__()
        assert (
            str_output
            == """
ID вакансии: 122377605
Название вакансии: Автомойщик
Ссылка: https://hh.ru/vacancy/122377605
Зарплата: 100000 - 150000
Навыки: Опыт работы на автомойке.
Обязанности: Профессиональная мойка кузова, дисков."""
        )

    def test__ge__(self, sample_vacancy_1: Vacancy, sample_vacancy_2: Vacancy) -> None:
        assert sample_vacancy_1.__ge__(sample_vacancy_2)

    def test__le__(self, sample_vacancy_1: Vacancy, sample_vacancy_2: Vacancy) -> None:
        assert sample_vacancy_1.__le__(sample_vacancy_2)

    def test_to_dict(self, sample_vacancy_1: Vacancy) -> None:
        vac_to_dict = sample_vacancy_1.to_dict()
        assert vac_to_dict == {
            "ID вакансии": "122377605",
            "Название вакансии": "Автомойщик",
            "Ссылка": "https://hh.ru/vacancy/122377605",
            "Зарплата": "100000 - 150000",
            "Навыки": "Опыт работы на автомойке.",
            "Обязанности": "Профессиональная мойка кузова, дисков.",
        }

    def test_create_vacancy(self, sample_vacancy_1: Vacancy) -> None:
        id_vacancy = "122497603"
        name_vacancy = "Водитель-экспедитор кат. 'В' на авто Форд, Ивеко (будки)"
        url = "https://hh.ru/vacancy/122497603"
        salary_from = 56000
        salary_to = 180000
        skills = "Наличие ИП. Опыт работы в сфере транспортно-экспедиторских услуг."
        responsibilities = "Выгрузка автомобиля (2-3 тонны) - силами водителя!"

        vac_2 = Vacancy.create_vacancy(id_vacancy, name_vacancy, url, salary_from, salary_to, skills, responsibilities)

        assert isinstance(vac_2, Vacancy)
