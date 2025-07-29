import json
import os.path

from src.config import FILE_PATH
from src.models.abstracts import BaseSaverVacancy
from src.models.vacancy import Vacancy


class JSONSaver(BaseSaverVacancy):
    """Класс для сохранения вакансий в файл формата JSON."""

    def __init__(self, filename: str = "vacancies.json") -> None:
        """Инициализация экземпляра класса JSONSaver"""
        self.__filename = os.path.join(FILE_PATH, filename)
        self._vacancies = self._read_file()

    @property
    def vacancies(self) -> list:
        """Возвращает текущие вакансии"""
        return self._vacancies

    def _read_file(self) -> list:
        """Если файл уже существует, то читает его и присваивает данные self.__vacancies"""
        if os.path.exists(self.__filename):
            if os.path.getsize(self.__filename) > 0:
                try:
                    with open(self.__filename, encoding="utf-8") as file:
                        res: list = json.load(file)
                        return res
                except json.JSONDecodeError:
                    print("Ошибка: файл содержит повреждённый JSON. Будет загружен пустой список.")
                    return []
        return []

    def write_vacancies(self, vacancies: list) -> None:
        """Записывает вакансии в файл"""
        try:
            vac_json = [vac.to_dict() if isinstance(vac, Vacancy) else vac for vac in vacancies]
            with open(self.__filename, "w", encoding="utf-8") as file:
                json.dump(vac_json, file, indent=4, ensure_ascii=False)  # type:ignore

        except TypeError:
            raise TypeError("Не получилось записать вакансии в файл формата json.")

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавляет вакансии в файл"""
        if not isinstance(vacancy, Vacancy):
            raise TypeError("Некорректные данные. Добавьте вакансию.")

        existing_ids = {vac.get("ID вакансии") for vac in self._vacancies}

        if vacancy.id_vacancy in existing_ids:
            print("Вакансия с таким ID существует.")
        else:
            self._vacancies.append(vacancy.to_dict())
            self.write_vacancies(self._vacancies)
            print("Вакансия успешно добавлена.")

    def remove_vacancies(self, vacancy_id: str) -> None:
        """Удаляет вакансии из списка по ID"""
        self._vacancies = [
            vac
            for vac in self._vacancies
            if (vac.get("ID вакансии") if isinstance(vac, dict) else vac.id_vacancy) != vacancy_id
        ]
        self.write_vacancies(self._vacancies)
        self._vacancies = self._read_file()
        print("Вакансия в файле json успешно удалена.")

    def clear(self) -> None:
        """Удаляет все вакансии"""
        self._vacancies = []
        self.write_vacancies([])
        print("Все вакансии удалены в json файле.")


class TXTSaver(BaseSaverVacancy):
    """Класс для сохранения вакансий в файл формата TXT."""

    def __init__(self, filename: str = "vacancies.txt") -> None:
        """Инициализация экземпляра класса TXTSaver"""
        self.__filename = os.path.join(FILE_PATH, filename)
        self._vacancies = self._read_file()

    @property
    def vacancies(self) -> str:
        """Возвращает текущие вакансии"""
        return self._vacancies

    def _read_file(self) -> str:
        """Если файл уже существует, то читает его и присваивает данные self.__vacancies"""
        if os.path.exists(self.__filename):
            if os.path.getsize(self.__filename) > 0:
                try:
                    with open(self.__filename, encoding="utf-8") as file:
                        return file.read()
                except (OSError, UnicodeDecodeError) as e:
                    print(f"Ошибка: txt файл не прочитан. Причина: {e}")
                    return ""
        return ""

    def write_vacancies(self, vacancies: list) -> None:
        """Записывает вакансии в файл"""
        try:
            with open(self.__filename, "a", encoding="utf-8") as file:
                for vac in vacancies:
                    if isinstance(vac, Vacancy):
                        id_vac = vac.id_vacancy
                        name = vac.name_vacancy
                        url = vac.url
                        salary = f"{vac.salary_from} - {vac.salary_to}"
                        skills = vac.skills
                        responsibilities = vac.responsibilities
                    else:
                        id_vac = vac.get("ID вакансии")
                        name = vac.get("Название вакансии")
                        url = vac.get("Ссылка")
                        salary = vac.get("Зарплата")
                        skills = vac.get("Навыки")
                        responsibilities = vac.get("Обязанности")

                    file.write(f"ID вакансии: {id_vac}\n")
                    file.write(f"Название вакансии: {name}\n")
                    file.write(f"Ссылка: {url}\n")
                    file.write(f"Зарплата: {salary}\n")
                    file.write(f"Навыки: {skills}\n")
                    file.write(f"Обязанности: {responsibilities}\n")
                    file.write("-" * 40 + "\n")
                self._vacancies = self._read_file()
        except Exception as e:
            raise RuntimeError(f"Не удалось сохранить вакансии в txt файл: {e}")

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавляет вакансии в файл"""
        if not isinstance(vacancy, Vacancy):
            raise TypeError("Некорректные данные. Добавьте вакансию.")

        new_vacancy = [vacancy]
        existing_ids = set()

        for line in self._vacancies.splitlines():
            if line.startswith("ID вакансии:"):
                existing_ids.add(line.split("ID вакансии:")[1].strip())

        if vacancy.id_vacancy in existing_ids:
            print("Вакансия с таким ID существует.")
        else:
            self.write_vacancies(new_vacancy)
            self._vacancies = self._read_file()
            print("Вакансия успешно добавлена.")

    def remove_vacancies(self, vacancy_id: str) -> None:
        """Удаляет информацию о вакансиях"""
        lines = self._vacancies.splitlines()
        new_lines = []
        flag_id = False

        for line in lines:
            if line.startswith("ID вакансии:") and line.split("ID вакансии:")[1].strip() == vacancy_id:
                flag_id = True
                continue

            if flag_id:
                if line.strip() == "-" * 40:
                    flag_id = False
                continue
            new_lines.append(line)

        with open(self.__filename, "w", encoding="utf-8") as file:
            file.write("\n".join(new_lines) + "\n")
        self._vacancies = self._read_file()
        print("Вакансия в файле txt успешно удалена.")
