from src.models.vacancy import Vacancy


class VacancySelector:
    """Класс для фильтрации, сортировки и выбора топ-N вакансий из списка"""

    def __init__(self, vacancies: list["Vacancy"]) -> None:
        """Инициализирует экземпляр класса VacancySelector"""
        self.vacancies = vacancies

    def filter_by_keywords(self, vacancies: list["Vacancy"], filter_words: str) -> list["Vacancy"]:
        """Фильтрует список вакансий по ключевым словам"""
        words = self.parse_filter_words(filter_words)
        if not words:
            return vacancies

        filtered = [
            vac
            for vac in vacancies
            if any(
                word in " ".join([vac.name_vacancy.lower(), vac.skills.lower(), vac.responsibilities.lower()])
                for word in words
            )
        ]
        return filtered

    def select_vacancies(
        self, filter_words: str | None = None, salary_range: str | None = None, top_n: int | None = None
    ) -> list["Vacancy"] | None:
        """Фильтрует, сортирует и выводит на экран топ вакансий по заданным критериям"""
        result = self.vacancies

        if filter_words:
            result = self.filter_by_keywords(result, filter_words)

        if salary_range:
            result = self.filter_by_salary_range(result, salary_range)

        result = self.sort_by_salary(result)

        if top_n:
            result = self.get_top(result, top_n)

        if not result:
            print("Нет объявлений по указанным критериям.")
        return result

    @staticmethod
    def safe_int_input(prompt: str, default: int = 0) -> int:
        """Возвращает только корректное число, введенное пользователем"""
        while True:
            value = input(prompt).strip()
            if not value:
                return default
            try:
                return int(value)
            except ValueError:
                print("Пожалуйста, введите корректное число.")

    @staticmethod
    def filter_by_salary_range(vacancies: list["Vacancy"], salary_range: str) -> list["Vacancy"]:
        """Фильтрует список вакансий по диапазону зарплат"""
        if not salary_range:
            return vacancies

        try:
            parts = salary_range.replace("-", " ").split()
            if len(parts) != 2:
                raise ValueError("Неверный формат диапазона зарплат. Пример: 100000 - 150000")

            salary_from, salary_to = map(int, parts)
            if salary_from > salary_to:
                salary_from, salary_to = salary_to, salary_from

        except ValueError as e:
            print(f"Ошибка в формате зарплат: {e}")
            return vacancies

        filtered = [vac for vac in vacancies if vac.salary_to >= salary_from and vac.salary_from <= salary_to]
        return filtered

    @staticmethod
    def parse_filter_words(filter_words: str) -> list:
        """Преобразует строку с ключевыми словами в список слов для фильтрации."""
        if not filter_words:
            return []

        words = [word.strip().lower() for word in filter_words.replace(",", " ").split()]
        return words

    @staticmethod
    def sort_by_salary(vacancies: list["Vacancy"]) -> list["Vacancy"]:
        """Сортирует список вакансий по убыванию зарплаты"""
        return sorted(vacancies, key=lambda vac: vac.salary_from, reverse=True)

    @staticmethod
    def get_top(vacancies: list["Vacancy"], top_n: int) -> list["Vacancy"]:
        """Возвращает количество вакансий которое указал пользователь"""
        if top_n <= 0:
            return vacancies
        return vacancies[:top_n]
