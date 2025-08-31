from contextlib import nullcontext as does_not_raise
from typing import ContextManager
from unittest.mock import mock_open, patch

import pytest

from src.models.vacancy import Vacancy
from src.services.savers import JSONSaver, TXTSaver


class TestJSONSaver:
    def test__init__(self, monkeypatch: pytest.MonkeyPatch, sample_vacancy_1: Vacancy) -> None:
        fake_vacancy_list = [sample_vacancy_1.to_dict()]
        monkeypatch.setattr(JSONSaver, "_read_file", lambda slf: fake_vacancy_list)
        saver = JSONSaver("test.json")

        assert saver.vacancies == fake_vacancy_list

    def test_write_vacancies(self, sample_vacancy_1: Vacancy) -> None:
        saver = JSONSaver("test.json")
        vacancies = [sample_vacancy_1]

        with patch("builtins.open", new_callable=mock_open) as mocked_file, patch("json.dump") as mock_json_dump:
            saver.write_vacancies(vacancies)

            mocked_file.assert_called_once_with(saver._JSONSaver__filename, "w", encoding="utf-8")  # type: ignore

            expected_json = [vac.to_dict() for vac in vacancies]
            mock_json_dump.assert_called_once_with(expected_json, mocked_file(), indent=4, ensure_ascii=False)

    @pytest.mark.parametrize(
        "data_file, res, expectation",
        [
            ([], "Вакансия успешно добавлена.\n", does_not_raise()),
            ([{"ID вакансии": "122377605"}], "Вакансия с таким ID существует.\n", does_not_raise()),
        ],
    )
    def test_add_vacancy(
        self,
        capsys: pytest.CaptureFixture,
        monkeypatch: pytest.MonkeyPatch,
        sample_vacancy_1: Vacancy,
        data_file: list,
        res: str,
        expectation: ContextManager,
    ) -> None:

        monkeypatch.setattr(JSONSaver, "_read_file", lambda slf: data_file.copy())
        monkeypatch.setattr(JSONSaver, "write_vacancies", lambda slf, vacancies: None)

        with expectation:
            saver = JSONSaver("test.json")
            saver.add_vacancy(sample_vacancy_1)

            captured = capsys.readouterr()
            assert captured.out == res

    def test_remove_vacancies(self, monkeypatch: pytest.MonkeyPatch, sample_vacancy_1: Vacancy) -> None:
        fake_id = sample_vacancy_1.id_vacancy
        fake_data = [sample_vacancy_1.to_dict()]

        current_data = fake_data.copy()

        def fake_read_file() -> list:
            return current_data

        def fake_write_vacancies(vacancies: list) -> None:
            nonlocal current_data
            current_data = vacancies

        monkeypatch.setattr(JSONSaver, "_read_file", lambda slf: fake_read_file())
        monkeypatch.setattr(JSONSaver, "write_vacancies", lambda slf, vacancies: fake_write_vacancies(vacancies))

        saver = JSONSaver("test.json")
        saver.remove_vacancies(fake_id)

        assert saver.vacancies == []


class TestTXTSaver:
    def test_initial_vacancies_empty(self, txt_saver: TXTSaver) -> None:
        assert txt_saver.vacancies == ""

    def test_write_vacancies_adds_content(self, txt_saver: TXTSaver, sample_vacancy_1: Vacancy) -> None:
        txt_saver.write_vacancies([sample_vacancy_1])

        with open(txt_saver.filename, encoding="utf-8") as f:
            content = f.read()
        assert "Автомойщик" in content

    def test_add_vacancy_new(self, txt_saver: TXTSaver, sample_vacancy_1: Vacancy) -> None:
        txt_saver.add_vacancy(sample_vacancy_1)
        content = txt_saver.vacancies
        assert "Автомойщик" in content
        assert "ID вакансии: 122377605" in content

    def test_add_vacancy_existing(
        self, txt_saver: TXTSaver, sample_vacancy_1: Vacancy, capsys: pytest.CaptureFixture
    ) -> None:
        txt_saver.add_vacancy(sample_vacancy_1)

        txt_saver.add_vacancy(sample_vacancy_1)
        captured = capsys.readouterr()
        assert "Вакансия с таким ID существует." in captured.out

    def test_remove_vacancy(self, txt_saver: TXTSaver, sample_vacancy_1: Vacancy) -> None:
        txt_saver.add_vacancy(sample_vacancy_1)
        txt_saver.remove_vacancies("122377605")
        content = txt_saver.vacancies
        assert "Автомойщик" not in content
        assert "ID вакансии: 122377605" not in content

    def test_remove_nonexistent_vacancy(
        self, txt_saver: TXTSaver, sample_vacancy_1: Vacancy, capsys: pytest.CaptureFixture
    ) -> None:
        txt_saver.remove_vacancies("999999")
        captured = capsys.readouterr()

        assert "успешно удалена" in captured.out or txt_saver.vacancies == ""
