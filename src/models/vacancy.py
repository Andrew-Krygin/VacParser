class Vacancy:
    """Класс для представления вакансий."""

    __slots__ = ("id_vacancy", "name_vacancy", "url", "skills", "responsibilities", "salary_from", "salary_to")

    def __init__(
        self,
        id_vacancy: str,
        name_vacancy: str,
        url: str,
        salary_from: int | float,
        salary_to: int | float,
        skills: str,
        responsibilities: str,
    ) -> None:
        """Инициализирует экземпляр класса Vacancy"""
        self.id_vacancy = id_vacancy or "ID не указан"
        self.name_vacancy = name_vacancy or "Имя не указано"
        self.url = url or "Ссылка не указана"
        self.skills = skills or "Нет описания"
        self.responsibilities = responsibilities or "Нет описания"
        self.salary_from = salary_from if isinstance(salary_from, (int, float)) else 0
        self.salary_to = salary_to if isinstance(salary_to, (int, float)) else 0

    def __str__(self) -> str:
        """Возвращает состояние объекта в конкретный момент времени."""
        salary_str = f"{self.salary_from}" if not self.salary_to else f"{self.salary_from} - {self.salary_to}"

        return f"""
ID вакансии: {self.id_vacancy}
Название вакансии: {self.name_vacancy}
Ссылка: {self.url}
Зарплата: {salary_str}
Навыки: {self.skills}
Обязанности: {self.responsibilities}"""

    def __ge__(self, other: object) -> bool:
        """Сравнивает зарплаты в вакансиях(>=)."""
        if isinstance(other, Vacancy):
            return self.salary_from >= other.salary_from
        elif isinstance(other, (int, float)):
            return self.salary_from >= other
        else:
            raise ValueError("Ошибка: невозможно сравнить зарплаты.")

    def __le__(self, other: object) -> bool:
        """Сравнивает зарплаты в вакансиях(<=)."""
        if isinstance(other, Vacancy):
            return self.salary_to <= other.salary_to
        elif isinstance(other, (int, float)):
            return self.salary_to <= other
        else:
            raise ValueError("Ошибка: невозможно сравнить зарплаты.")

    def to_dict(self) -> dict:
        """Сериализует экземпляр класса в словарь"""
        salary_str = f"{self.salary_from}" if not self.salary_to else f"{self.salary_from} - {self.salary_to}"

        return {
            "ID вакансии": self.id_vacancy,
            "Название вакансии": self.name_vacancy,
            "Ссылка": self.url,
            "Зарплата": salary_str,
            "Навыки": self.skills,
            "Обязанности": self.responsibilities,
        }

    @classmethod
    def create_vacancy(
        cls,
        id_vacancy: str,
        name_vacancy: str,
        url: str,
        salary_from: int | float,
        salary_to: int | float,
        skills: str,
        responsibilities: str,
    ) -> "Vacancy":
        """Создает экземпляр класса Vacancy"""
        return cls(id_vacancy, name_vacancy, url, salary_from, salary_to, skills, responsibilities)
