import json
from unittest.mock import MagicMock, patch

import pytest
import requests

from src.models.vacancy import Vacancy
from src.services.head_hunter_api import HeadHunterApi


class TestHeadHunterApi:
    def test_connect_api_success(self, monkeypatch: pytest.MonkeyPatch) -> None:
        api = HeadHunterApi()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"items": []}

        monkeypatch.setattr("requests.get", lambda *_, **__: mock_response)

        data = api._connect_api("python")
        assert isinstance(data, dict)
        assert "items" in data

    def test_connect_api_http_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        api = HeadHunterApi()
        mock_response = MagicMock()
        mock_response.status_code = 500

        monkeypatch.setattr("requests.get", lambda *_, **__: mock_response)

        with pytest.raises(requests.exceptions.HTTPError):
            api._connect_api("python")

    def test_connect_api_invalid_json(self, monkeypatch: pytest.MonkeyPatch) -> None:
        api = HeadHunterApi()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.side_effect = json.JSONDecodeError("Expecting value", "", 0)

        monkeypatch.setattr("requests.get", lambda *_, **__: mock_response)

        with pytest.raises(Exception) as exc_info:
            api._connect_api("python")
        assert "декодирования" in str(exc_info.value)

    def test_get_vacancies_calls_convert(self, monkeypatch: pytest.MonkeyPatch) -> None:
        api = HeadHunterApi()
        dummy_data = {"items": [{"id": "123", "name": "Dev"}]}
        monkeypatch.setattr(api, "_connect_api", lambda _: dummy_data)

        with patch.object(HeadHunterApi, "_HeadHunterApi__convert_to_vacancies", return_value=["vac"]) as mock_convert:
            result = api.get_vacancies("python")
            assert result == ["vac"]
            mock_convert.assert_called_once_with(dummy_data)

    def test_convert_to_vacancies_creates_objects(self) -> None:
        data = {
            "items": [
                {
                    "id": "1",
                    "name": "Python Dev",
                    "alternate_url": "http://test",
                    "snippet": {"requirement": "<b>Python</b> knowledge", "responsibility": "Develop <i>apps</i>"},
                    "salary": {"from": 100000, "to": 150000},
                }
            ]
        }

        vacancies = HeadHunterApi._HeadHunterApi__convert_to_vacancies(data)  # type: ignore
        vac = vacancies[0]
        assert isinstance(vac, Vacancy)
        assert vac.name_vacancy == "Python Dev"
        assert "Python" in vac.skills
        assert "Develop apps" in vac.responsibilities

    def test_convert_to_vacancies_with_empty_fields(self) -> None:
        data = {"items": [{"id": "2", "alternate_url": "http://test", "snippet": {}}]}
        vacancies = HeadHunterApi._HeadHunterApi__convert_to_vacancies(data)  # type: ignore
        vac = vacancies[0]
        assert vac.id_vacancy == "2"
        assert vac.name_vacancy == "Не указано"
        assert vac.salary_from == 0
        assert vac.salary_to == 0
        assert vac.skills == "Нет описания"
        assert vac.responsibilities == "Нет описания"
