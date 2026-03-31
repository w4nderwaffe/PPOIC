from dataclasses import dataclass, field


@dataclass
class StudentRecord:
    full_name: str
    group: str
    social_work: list[int] = field(default_factory=list)

    def __post_init__(self):
        self.full_name = self.full_name.strip()
        self.group = self.group.strip()

        if len(self.social_work) != 10:
            raise ValueError("Список общественной работы должен содержать 10 значений")

        normalized = []
        for value in self.social_work:
            number = int(value)
            if number < 0:
                raise ValueError("Значения общественной работы не могут быть отрицательными")
            normalized.append(number)

        self.social_work = normalized

        if not self.full_name:
            raise ValueError("ФИО не может быть пустым")

        if not self.group:
            raise ValueError("Группа не может быть пустой")

    @property
    def surname(self) -> str:
        parts = self.full_name.split()
        return parts[0] if parts else ""

    @property
    def total_social_work(self) -> int:
        return sum(self.social_work)
