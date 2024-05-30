# exam.py
from typing import Optional


class Exam:
    def __init__(self, name: str, passing_score: int):
        self.name = name
        self.passing_score = passing_score
        self.scores = []

    def add_score(self, score: int) -> None:
        self.scores.append(score)

    def last_score(self) -> Optional[int]:
        if not self.scores:
            return None
        return self.scores[-1]

    def has_passed(self) -> bool:
        last_score = self.last_score()
        if last_score is None:
            return False
        return last_score >= self.passing_score

    def __str__(self) -> str:
        if not self.scores:
            return f"Экзамен {self.name} (нет оценок)"
        return f"Экзамен {self.name} (оценки: {self.scores})"