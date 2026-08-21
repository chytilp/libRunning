from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal


@dataclass
class Grade:
    grade: int
    from_: Decimal
    to_: Decimal
    time_convertible: bool = True

    @property
    def reverse(self) -> bool:
        return self.to_ < self.from_

    def match(self, value: int) -> bool:
        if not self.reverse:
            return self.from_ <= value < self.to_
        else:
            return self.from_ >= value > self.to_

    @property
    def tuple(self) -> tuple[Decimal, Decimal]:
        return self.from_, self.to_

    @staticmethod
    def _convert_to_decimal(value: int) -> Decimal:
        return Decimal(str(value))

    @staticmethod
    def create(grade: int, from_: int, to_: int, time_convertible: bool = True) -> Grade:
        return Grade(grade, Grade._convert_to_decimal(from_), Grade._convert_to_decimal(to_),
                     time_convertible)


@dataclass
class Grades:
    grades: dict[int, Grade] = field(default_factory=dict)
    time_convertible: bool = True
    less_is_best: bool = True

    @property
    def empty(self) -> bool:
        return len(self.grades) == 0

    def add(self, grade: Grade) -> None:
        if grade.grade < 1 or grade.grade > 5:
            raise ValueError(f"Grade {grade.grade} is out of range")

        self.grades[grade.grade] = grade

    def get_grade(self, grade: int) -> Grade | None:
        if grade < 1 or grade > 5:
            raise ValueError(f"Grade {grade} is out of range")

        return self.grades.get(grade)

    def grade_1(self) -> Grade:
        if 1 not in self.grades:
            raise ValueError("Grade 1 not found.")

        return self.grades[1]

    def grade_2(self) -> Grade:
        if 2 not in self.grades:
            raise ValueError("Grade 2 not found.")

        return self.grades[2]

    def grade_3(self) -> Grade:
        if 3 not in self.grades:
            raise ValueError("Grade 3 not found.")

        return self.grades[3]

    def grade_4(self) -> Grade:
        if 4 not in self.grades:
            raise ValueError("Grade 4 not found.")

        return self.grades[4]

    def grade_5(self) -> Grade:
        if 5 not in self.grades:
            raise ValueError("Grade 5 not found.")

        return self.grades[5]

    def get_aggregation_dict(self) -> dict[int, tuple[Decimal, Decimal, bool]]:
        return {
            1: (self.grade_1().from_, self.grade_1().to_, self.time_convertible),
            2: (self.grade_2().from_, self.grade_2().to_, self.time_convertible),
            3: (self.grade_3().from_, self.grade_3().to_, self.time_convertible),
            4: (self.grade_4().from_, self.grade_4().to_, self.time_convertible),
            5: (self.grade_5().from_, self.grade_5().to_, self.time_convertible),
        }

    def get_section_dict(self) -> dict[int, tuple[Decimal, Decimal]]:
        return {
            1: (self.grade_1().from_, self.grade_1().to_),
            2: (self.grade_2().from_, self.grade_2().to_),
            3: (self.grade_3().from_, self.grade_3().to_),
            4: (self.grade_4().from_, self.grade_4().to_),
            5: (self.grade_5().from_, self.grade_5().to_),
        }

    def get_grade_match(self, value: int) -> int | None:
        grade_numbers = [1, 2, 3, 4, 5]
        for grade_num in grade_numbers:
            g = self.grades.get(grade_num)
            if g is not None:
                match_ok = g.match(value)
                if match_ok:
                    return grade_num
        return None
