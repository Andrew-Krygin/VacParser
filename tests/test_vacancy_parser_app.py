from unittest.mock import MagicMock, patch

import pytest

from src.app.vacancy_parser_app import VacancyParserApp
from src.models.vacancy import Vacancy
from tests.conftest import DummySaver


class TestVacancyParserApp:
    def test_process_save_choice_saves(self, app: VacancyParserApp) -> None:
        vacancies = ["Vacancy1"]
        app.process_save_choice("1", vacancies)
        saver = app.savers["1"]
        assert isinstance(saver, DummySaver)
        assert saver.saved
        assert "Vacancy1" in saver.vacancies

    def test_process_save_choice_prints(self, capsys: pytest.CaptureFixture, app: VacancyParserApp) -> None:
        vacancies = ["Vacancy2"]
        app.process_save_choice("3", vacancies)
        captured = capsys.readouterr()
        assert "Vacancy2" in captured.out

    def test_get_valid_choice_valid(self, monkeypatch: pytest.MonkeyPatch, app: VacancyParserApp) -> None:
        monkeypatch.setattr("builtins.input", lambda _: "1")
        choice = app.get_valid_choice("prompt", {"1", "2"})
        assert choice == "1"

    def test_get_valid_choice_invalid(
        self, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture, app: VacancyParserApp
    ) -> None:
        inputs = iter(["x", "1"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        choice = app.get_valid_choice("prompt", {"1", "2"})
        captured = capsys.readouterr()
        assert "Неверный выбор" in captured.out
        assert choice == "1"

    def test_should_stay_in_menu_yes(self, monkeypatch: pytest.MonkeyPatch, app: VacancyParserApp) -> None:
        monkeypatch.setattr("builtins.input", lambda _: "да")
        assert app.should_stay_in_menu()

    def test_should_stay_in_menu_no(self, monkeypatch: pytest.MonkeyPatch, app: VacancyParserApp) -> None:
        monkeypatch.setattr("builtins.input", lambda _: "нет")
        assert not app.should_stay_in_menu()

    def test_print_vacancies_empty(self, capsys: pytest.CaptureFixture, app: VacancyParserApp) -> None:
        app.print_vacancies([])
        captured = capsys.readouterr()
        assert "Нет сохранённых вакансий" in captured.out

    def test_print_vacancies_list(self, capsys: pytest.CaptureFixture, app: VacancyParserApp) -> None:
        app.print_vacancies(["VacancyX"])
        captured = capsys.readouterr()
        assert "VacancyX" in captured.out

    def test_handle_search_vacancies_found(
        self, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture, app: VacancyParserApp
    ) -> None:
        mock_api = MagicMock()
        mock_api.get_vacancies.return_value = ["raw_vacancy"]
        mock_selector = MagicMock()
        mock_selector.select_vacancies.return_value = ["filtered_vacancy"]
        app.hh_api = mock_api

        with patch("src.app.vacancy_parser_app.VacancySelector", return_value=mock_selector):
            inputs = iter(["python", "Django", "100000 - 150000", "5"])
            monkeypatch.setattr("builtins.input", lambda _: next(inputs))

            with patch.object(app, "ask_to_save") as mock_ask_to_save:
                app.handle_search_vacancies()

                mock_api.get_vacancies.assert_called_once_with("python")
                mock_selector.select_vacancies.assert_called_once()
                mock_ask_to_save.assert_called_once_with(["filtered_vacancy"])

                captured = capsys.readouterr()
                assert "Найдено" in captured.out

    def test_handle_search_vacancies_not_found(
        self, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture, app: VacancyParserApp
    ) -> None:
        mock_api = MagicMock()
        mock_api.get_vacancies.return_value = ["raw_vacancy"]
        mock_selector = MagicMock()
        mock_selector.select_vacancies.return_value = []
        app.hh_api = mock_api

        with patch("src.app.vacancy_parser_app.VacancySelector", return_value=mock_selector):
            inputs = iter(["python", "Flask", "50000 - 70000", "5"])
            monkeypatch.setattr("builtins.input", lambda _: next(inputs))
            app.handle_search_vacancies()
            captured = capsys.readouterr()
            assert "не найдены" in captured.out

    def test_ask_to_save_saves_and_exits(self, monkeypatch: pytest.MonkeyPatch, app: VacancyParserApp) -> None:
        vacancies = ["vac1"]
        inputs = iter(["1", "нет"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        with patch.object(app, "process_save_choice") as mock_method:
            app.ask_to_save(vacancies)
            mock_method.assert_called_once_with("1", vacancies)

    def test_run_exit_immediately(self, app: VacancyParserApp) -> None:
        with patch("builtins.input", side_effect=["5"]), patch("sys.exit") as mock_exit:
            app.run()
            mock_exit.assert_called_once()

    def test_ask_to_save_exit(self, app: VacancyParserApp, sample_vacancy_2: Vacancy) -> None:
        with patch("builtins.input", side_effect=["3", "4"]):
            app.ask_to_save([sample_vacancy_2])

    def test_handle_show_saved_vacancies_exit(
        self, app: VacancyParserApp, dummy_savers: dict, sample_vacancy_2: Vacancy
    ) -> None:
        dummy_savers["1"].vacancies.append(sample_vacancy_2)
        with patch("builtins.input", side_effect=["1", "3"]):
            app.handle_show_saved_vacancies()

    def test_handle_add_vacancies_exit(self, app: VacancyParserApp, sample_vacancy_2: Vacancy) -> None:
        inputs = [
            "1",
            sample_vacancy_2.id_vacancy,
            sample_vacancy_2.name_vacancy,
            sample_vacancy_2.url,
            str(sample_vacancy_2.salary_from),
            str(sample_vacancy_2.salary_to),
            sample_vacancy_2.skills,
            sample_vacancy_2.responsibilities,
            "нет",
        ]
        with patch("builtins.input", side_effect=inputs):
            app.handle_add_vacancies()

    def test_handle_delete_vacancy_exit(
        self, app: VacancyParserApp, dummy_savers: dict, sample_vacancy_2: Vacancy
    ) -> None:
        dummy_savers["1"].vacancies.append(sample_vacancy_2)

        inputs = [sample_vacancy_2.id_vacancy, "1", "нет"]
        with patch("builtins.input", side_effect=inputs):
            app.handle_delete_vacancy()
        assert dummy_savers["1"].removed_id == sample_vacancy_2.id_vacancy
