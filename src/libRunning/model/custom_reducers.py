from math import ceil
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


def median(values: list[int]) -> int:
    sorted_values: list[int] = sorted(values)
    if len(sorted_values) % 2 != 0:
        mid = len(sorted_values) // 2
        return sorted_values[mid]
    else:
        mid_1 = len(sorted_values) // 2
        mid_2 = mid_1 - 1
        result =  (sorted_values[mid_1] + sorted_values[mid_2]) / 2
        int_result = int(result)
        if result - int_result == 0.5:
            return ceil(result)
        return round(result)
