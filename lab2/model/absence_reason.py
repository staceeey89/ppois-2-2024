import uuid
from typing import Optional


class AbsenceReason:
    def __init__(self, id: uuid.UUID, name: str, desc: Optional[str]) -> None:
        self.id = id
        self.name = name
        self.desc = desc

    def __str__(self) -> str:
        return f'{self.id}, Absence reason: {self.name}, {self.desc}'
