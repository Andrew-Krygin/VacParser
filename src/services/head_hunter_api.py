import json
import re

import requests

from src.models.abstracts import BaseApi
from src.models.vacancy import Vacancy


class HeadHunterApi(BaseApi):
    """Класс для работы с API hh.ru"""

    BASE_URL = "https://api.hh.ru/vacancies"
    AREA = 113
    PER_PAGE = 100

    def _connect_api(self, query: str) -> dict:
        """Подключается к API hh.ru"""
        params: dict[str, str | int] = {"text": query, "per_page": self.PER_PAGE, "area": self.AREA}

        response = requests.get(self.BASE_URL, params=params)

        if response.status_code != 200:
            raise requests.exceptions.HTTPError(f"Ошибка запроса к hh.ru API: {response.status_code}")

        try:
            data: dict = response.json()
            return data
        except json.JSONDecodeError:
            raise Exception("Ошибка декодирования данных при получении ответа от API hh.ru")

    def get_vacancies(self, query: str) -> list:
        """Получает вакансии с hh.ru по API."""
        data = self._connect_api(query)
        vacancies = self.__convert_to_vacancies(data)

        return vacancies

    @staticmethod
    def __convert_to_vacancies(data: dict) -> list:
        """Преобразует список словарей с вакансиями в список экземпляров класса Vacancy"""

        vacancies = []

        for vacancy in data.get("items", []):
            id_vacancy = vacancy.get("id", "ID не указан")
            name_vacancy = vacancy.get("name", "Не указано")
            url = vacancy.get("alternate_url", "Ссылка не указана")

            raw_skills = vacancy.get("snippet", {}).get("requirement") or "Нет описания"
            skills = re.sub(r"<.*?>", "", raw_skills)

            raw_responsibilities = vacancy.get("snippet", {}).get("responsibility") or "Нет описания"
            responsibilities = re.sub(r"<.*?>", "", raw_responsibilities)

            salary = vacancy.get("salary") or {}
            salary_from = salary.get("from", 0)
            salary_to = salary.get("to", 0)

            vacancies.append(Vacancy(id_vacancy, name_vacancy, url, salary_from, salary_to, skills, responsibilities))

        return vacancies
