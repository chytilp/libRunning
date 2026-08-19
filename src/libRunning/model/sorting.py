from dataclasses import dataclass


@dataclass
class SortResult:
    order: int
    lost: int
    grade: int
    time_convertible: bool = True
    less_is_best: bool = True

    def __post_init__(self) -> None:
        if self.grade not in [-1, 1, 2, 3, 4, 5]:
            raise ValueError(f'Invalid grade {self.grade}')
        # if self.lost < -1:
        #     raise ValueError(f'Invalid lost {self.lost}')
        if self.order == 0 or self.order < -1:
            raise ValueError(f'Invalid order {self.order}')
