from src.app.vacancy_parser_app import VacancyParserApp


def main() -> None:
    """
    Точка входа для приложения Vacancy Parser.Инициализирует и запускает экземпляр VacancyParserApp,
    запуская интерактивный цикл команд.
    """
    app = VacancyParserApp()
    app.run()


if __name__ == "__main__":
    main()
