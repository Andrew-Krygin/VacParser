from abc import ABC, abstractmethod

from src.models.vacancy import Vacancy


class BaseApi(ABC):
    """Абстрактный класс для работы с API сервиса с вакансиями."""

    @abstractmethod
    def _connect_api(self, query: str) -> dict:
        pass

    @abstractmethod
    def get_vacancies(self, query: str) -> list:
        """Метод позволяет подключаться к API и получать вакансии."""
        pass


class BaseSaverVacancy(ABC):
    """Абстрактный класс обязывает реализовать методы для добавления вакансий в файл, получения данных из файла по
    указанным критериям и удаления информации о вакансиях."""

    @abstractmethod
    def _read_file(self) -> list:
        """Если файл уже существует, то читает его и присваивает данные self.__vacancies"""
        pass

    @abstractmethod
    def write_vacancies(self, vacancies: list) -> None:
        """Получает данные из файла по указанным критериям"""
        pass

    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавляет вакансию в файл"""
        pass

    @abstractmethod
    def remove_vacancies(self, vacancy_id: str) -> None:
        """Удаляет информацию о вакансиях"""
        pass
