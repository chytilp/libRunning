import operator
from dataclasses import dataclass, field
from enum import StrEnum
from math import ceil


@dataclass
class Filter:
    operator: str
    value: int

    def __post_init__(self) -> None:
        if self.operator not in ['<', '>', '==', '!=', '<=', '>=']:
            raise ValueError(f'Invalid operator {self.operator}')

    def passed_value_through_filter(self, value: int) -> bool:
        d = {
            '<': operator.lt,
            '>': operator.gt,
            '==': operator.eq,
            '!=': operator.ne,
            '<=': operator.le,
            '>=': operator.ge,
        }
        output = d[self.operator](value, self.value)
        assert isinstance(output, bool)
        return output

    def passed_values_through_filter(self, values: list[int]) -> list[int]:
        return [value for value in values if self.passed_value_through_filter(value)]


class SortDefinition(StrEnum):
    LESS_IS_BEST = "less_is_best"
    MORE_IS_BEST = "more_is_best"


@dataclass
class AggregationDesc:
    name: str
    reducer: str
    inputs: list[str] = field(default_factory=list)
    filters: list[Filter] = field(default_factory=list)
    sort_definition: SortDefinition = SortDefinition.LESS_IS_BEST
    time_convertible: bool = True
    all_inputs_needed: bool = True

    def apply_reducer(self, values: list[int]) -> int:
        match self.reducer:
            case "sum":
                return sum(values)
            case "len":
                return len(values)
            case "min":
                return min(values)
            case "max":
                return max(values)
            case "avg":
                result = sum(values) / len(values)
                int_result = sum(values) // len(values)
                if result - int_result == 0.5:
                    return ceil(result)
                return round(result)
        return -1

    def apply_filters(self, values: list[int]) -> list[int]:
        tmp = values
        if self.filters:
            for filter_ in self.filters:
                tmp = filter_.passed_values_through_filter(tmp)
        return tmp

    @property
    def reverse(self) -> bool:
        return self.sort_definition == SortDefinition.MORE_IS_BEST
