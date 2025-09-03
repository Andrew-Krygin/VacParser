from src.services.vacancy_selector import VacancySelector


class TestVacancySelector:
    def test_filter_by_keywords(self, sample_selector: VacancySelector, sample_vacancies: list) -> None:
        result = sample_selector.filter_by_keywords(sample_vacancies, "Python")
        assert len(result) == 2
        assert all(
            "python" in " ".join([vac.name_vacancy.lower(), vac.skills.lower(), vac.responsibilities.lower()])
            for vac in result
        )

    def test_filter_by_keywords_no_match(self, sample_selector: VacancySelector, sample_vacancies: list) -> None:
        result = sample_selector.filter_by_keywords(sample_vacancies, "Ruby")
        assert len(result) == 0

    def test_filter_by_salary_range(self, sample_selector: VacancySelector, sample_vacancies: list) -> None:
        result = sample_selector.filter_by_salary_range(sample_vacancies, "80000 - 120000")
        assert len(result) == 1

    def test_filter_by_salary_range_no_match(self, sample_selector: VacancySelector, sample_vacancies: list) -> None:
        result = sample_selector.filter_by_salary_range(sample_vacancies, "150000 - 160000")
        assert len(result) == 0

    def test_sort_by_salary(self, sample_selector: VacancySelector, sample_vacancies: list) -> None:
        result = sample_selector.sort_by_salary(sample_vacancies)
        assert result[0].salary_from == 95000
        assert result[-1].salary_from == 60000

    def test_get_top_vacancies(self, sample_selector: VacancySelector, sample_vacancies: list) -> None:
        result = sample_selector.get_top(sample_vacancies, 3)
        assert len(result) == 3
        assert result[0].name_vacancy == "Data Scientist"

    def test_get_top_vacancies_zero(self, sample_selector: VacancySelector, sample_vacancies: list) -> None:
        result = sample_selector.get_top(sample_vacancies, 0)
        assert len(result) == 5

    def test_get_top_vacancies_negative(self, sample_selector: VacancySelector, sample_vacancies: list) -> None:
        result = sample_selector.get_top(sample_vacancies, -1)
        assert len(result) == 5
