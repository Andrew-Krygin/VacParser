import sys

from src.config import VALID_FILE_CHOICES, VALID_SAVE_CHOICES
from src.menus import ADD_VACANCIES_MENU, DELETE_FILE_MENU, MAIN_MENU, SAVE_MENU, SHOW_FILE_MENU
from src.models.vacancy import Vacancy
from src.services.head_hunter_api import HeadHunterApi
from src.services.savers import JSONSaver, TXTSaver
from src.services.vacancy_selector import VacancySelector

SAVERS = {"1": JSONSaver(), "2": TXTSaver()}


class VacancyParserApp:
    def __init__(self, api: HeadHunterApi | None = None, savers: dict | None = None) -> None:
        """Инициализация экземпляра класса VacancyParserApp"""
        self.hh_api = api or HeadHunterApi()
        self.savers = savers or SAVERS

    def run(self) -> None:
        """
        Запускает основной цикл приложения:
        - отображает главное меню, обрабатывает пользовательский ввод и перенаправляет к соответствующим обработчикам.
        - завершается при выборе выхода или прерывании программы.
        """
        try:
            while True:
                print(MAIN_MENU)
                choice = self.get_valid_choice("Выберите пункт: ", VALID_SAVE_CHOICES)

                match choice:
                    case "1":
                        self.handle_search_vacancies()
                    case "2":
                        self.handle_show_saved_vacancies()
                    case "3":
                        self.handle_add_vacancies()
                    case "4":
                        self.handle_delete_vacancy()
                    case "5":
                        self.exit_app()
                    case _:
                        print("Неверный ввод. Попробуйте снова.")
        except KeyboardInterrupt:
            print("\nВыход из приложения по запросу пользователя.")
        except Exception as e:
            print(f"Произошла непредвиденная ошибка: {e}")

    def handle_search_vacancies(self) -> None:
        """Осуществляет поиск вакансий по указанным критериям"""
        query = input("Введите поисковый запрос: ").strip()
        filter_words = input("Введите ключевые слова для фильтрации вакансий: ").strip()
        salary_range = input("Введите диапазон зарплат(пр.: 100000 - 150000): ").strip()
        top_n = VacancySelector.safe_int_input("Сколько топ вакансий вывести? ")

        raw_vacancies = self.hh_api.get_vacancies(query)
        selector = VacancySelector(raw_vacancies)
        filtered_vacancies = selector.select_vacancies(
            filter_words=filter_words, salary_range=salary_range, top_n=top_n
        )

        if filtered_vacancies:
            print(f"\nНайдено {len(filtered_vacancies)} вакансий:")
            self.ask_to_save(filtered_vacancies)
        else:
            print("Вакансии по заданным критериям не найдены.")

    def process_save_choice(self, choice: str, vacancies: list) -> None:
        """Осуществляет запись вакансий в файл или выводит их на экран"""
        if choice in {"1", "2"}:
            self.savers[choice].write_vacancies(vacancies)
            print("Вакансии сохранены.")
        elif choice == "3":
            self.print_vacancies(vacancies)

    def ask_to_save(self, vacancies: list) -> None:
        """Выводит меню сохранения и обрабатывает выбор: сохранение вакансий или вывод на экран"""
        while True:
            print(SAVE_MENU)
            choice = self.get_valid_choice("Ваш выбор: ", VALID_SAVE_CHOICES)
            if choice == "4":
                return
            self.process_save_choice(choice, vacancies)
            if not self.should_stay_in_menu():
                return

    def handle_show_saved_vacancies(self) -> None:
        """Показывает меню выбора файла и выводит сохранённые вакансии на экран."""
        while True:
            print(SHOW_FILE_MENU)
            choice = self.get_valid_choice("Выбор: ", VALID_FILE_CHOICES)
            if choice == "3":
                return
            vacancies = self.savers[choice].vacancies
            self.print_vacancies(vacancies)
            if not self.should_stay_in_menu():
                return

    def handle_add_vacancies(self) -> None:
        """Показывает меню выбора файла и сохраняет введенные вручную вакансии в указанный файл"""
        while True:
            print(ADD_VACANCIES_MENU)
            choice = self.get_valid_choice("Выбор: ", VALID_FILE_CHOICES)
            if choice == "3":
                return
            vacancy = self.get_data_user_for_vacancy()
            self.savers[choice].add_vacancy(vacancy)
            if not self.should_stay_in_menu():
                return

    def handle_delete_vacancy(self) -> None:
        """Показывает меню выбора файла и удаляет вакансии из указанного файла"""
        while True:
            vacancy_id = input("\nВведите ID вакансии для удаления: ").strip()
            print(DELETE_FILE_MENU)
            choice = self.get_valid_choice("Выбор: ", VALID_FILE_CHOICES)
            if choice == "3":
                return
            self.savers[choice].remove_vacancies(vacancy_id)
            if not self.should_stay_in_menu():
                return

    @staticmethod
    def get_data_user_for_vacancy() -> Vacancy:
        """Запрашивает у пользователя данные и возвращает экземпляр класса Vacancy"""
        print("\nВведите данные вакансии:")
        id_vacancy = input("ID вакансии: ").strip()
        name = input("Название вакансии: ").strip()
        url = input("Ссылка: ").strip()

        while True:
            try:
                salary_from = int(input("Зарплата от: ").strip())
                salary_to = int(input("Зарплата до: ").strip())
                break
            except ValueError:
                print("Ошибка: зарплата должна быть числом. Попробуйте снова.")

        skills = input("Навыки (через запятую): ").strip()
        responsibilities = input("Обязанности: ").strip()

        vac = Vacancy(id_vacancy, name, url, salary_from, salary_to, skills, responsibilities)
        return vac

    @staticmethod
    def get_valid_choice(prompt: str, valid_choices: set[str]) -> str:
        """Запрашивает ввод до тех пор, пока не введут допустимое значение"""
        while True:
            choice = input(prompt).strip().lower()
            if choice in valid_choices:
                return choice
            print("Неверный выбор. Повторите.")

    @staticmethod
    def should_stay_in_menu() -> bool:
        """Спрашивает у пользователя, хочет ли он остаться в текущем меню"""
        choice = input("\nОстаться в этом меню (да/нет): ").strip().lower()
        return choice in {"да", "д", "yes", "y"}

    @staticmethod
    def print_vacancies(vacancies: list | str) -> None:
        """Выводит вакансии на экран"""
        if not vacancies:
            print("Нет сохранённых вакансий.")
            return
        if isinstance(vacancies, str):
            print(vacancies)
        else:
            for vac in vacancies:
                print(vac)

    @staticmethod
    def exit_app() -> None:
        """Выходит из программы"""
        print("Выход из приложения.")
        sys.exit()
