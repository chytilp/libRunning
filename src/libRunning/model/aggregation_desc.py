from __future__ import annotations
import operator
from dataclasses import dataclass, field
from enum import StrEnum
from math import ceil
from typing import Any
from libRunning.model.custom_reducers import grade_points


@dataclass
class Filter:
    operator: str
    value: int
    field: str = "value"

    def __post_init__(self) -> None:
        if self.operator not in ['<', '>', '==', '!=', '<=', '>=']:
            raise ValueError(f'Invalid operator {self.operator}')

    def passed_value_through_filter(self, value: dict[str, Any]) -> bool:
        d = {
            '<': operator.lt,
            '>': operator.gt,
            '==': operator.eq,
            '!=': operator.ne,
            '<=': operator.le,
            '>=': operator.ge,
        }
        output = d[self.operator](value[self.field], self.value)
        assert isinstance(output, bool)
        return output

    def passed_values_through_filter(self, values: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return [value for value in values if self.passed_value_through_filter(value)]

    def __hash__(self) -> int:
        return hash(f"{self.operator},{self.value}")

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Filter):
            return False
        return hash(self) == hash(other)


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
    compute_with_field: str = "value"

    def apply_reducer(self, values: list[dict[str, int]]) -> int:
        match self.reducer:
            case "sum":
                return sum(item[self.compute_with_field] for item in values)
            case "len":
                return len(values)
            case "min":
                return min(item[self.compute_with_field] for item in values)
            case "max":
                return max(item[self.compute_with_field] for item in values)
            case "avg":
                result = sum(item[self.compute_with_field] for item in values) / len(values)
                int_result = sum(item[self.compute_with_field] for item in values) // len(values)
                if result - int_result == 0.5:
                    return ceil(result)
                return round(result)
            case "grade_points":
                return grade_points(values)
        return -1

    def apply_filters(self, values: list[dict[str, Any]]) -> list[dict[str, Any]]:
        tmp = values
        if self.filters:
            for filter_ in self.filters:
                tmp = filter_.passed_values_through_filter(tmp)
        return tmp

    @property
    def reverse(self) -> bool:
        return self.sort_definition == SortDefinition.MORE_IS_BEST

    @property
    def is_it_template(self) -> bool:
        return self.name.startswith("@")

    def copy(self, inputs: list[str], name: str) -> AggregationDesc:
        return AggregationDesc(
            name=name,
            reducer=self.reducer,
            inputs=inputs,
            filters=self.filters,
            sort_definition=self.sort_definition,
            time_convertible=self.time_convertible,
            all_inputs_needed=self.all_inputs_needed,
            compute_with_field=self.compute_with_field,
        )