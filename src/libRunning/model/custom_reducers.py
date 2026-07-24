from typing import Any


def grade_points(values: list[dict[str, Any]]) -> int:
    points: dict[int, int] = {
        1: 4,
        2: 3,
        3: 2,
        4: 1,
        5: 0,
    }
    return sum(points[int(value["grade"])] for value in values)