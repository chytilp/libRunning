from typing import Any, Protocol

from libRunning.model.aggregation_desc import AggregationDesc


def _sum_sections(data: dict[str, Any], training: str, sections: list[str]) -> tuple[bool, int]:
    sections_data: dict = data["trainings"][training]["sections"]
    inputs: list[int] = []
    for input_section in sections:
        if input_section not in sections_data.keys():
            return False, 0
        inputs.append(data["trainings"][training]["sections"][input_section]["value"])
    return True, sum(inputs)


def _load_data(data: dict[str, Any], training: str, sections: list[str], all_inputs_needed: bool) -> tuple[bool, list[int]]:
    sections_data: dict = data["trainings"][training]["sections"]
    inputs: list[int] = []
    for input_section in sections:
        if input_section not in sections_data.keys() and all_inputs_needed:
            return False, []

        if input_section in sections_data.keys():
            inputs.append(data["trainings"][training]["sections"][input_section]["value"])
    return True, inputs


def _sum_intervals(data: dict[str, Any], training: str, indexes: list[int]) -> tuple[bool, int]:
    if "intervals" not in data["trainings"][training].keys():
        return False, 0
    intervals_data: list[int] = data["trainings"][training]["intervals"]["values"]
    values: list[int] = []
    for index in indexes:
        try:
            values.append(intervals_data[index])
        except IndexError:
            return False, 0
    return True, sum(values)


class CalculateAggregationFunc(Protocol):
    def __call__(self, data: dict[str, Any], training: str, aggregation_type: str) -> dict[str, Any] | None:
        ...


def create_calculate_aggregation(aggregations_def: dict[str, AggregationDesc]) -> CalculateAggregationFunc:

    def prepare_output(ok: bool, result: int) -> dict[str, Any]:
        if not ok:
            return {}
        return {"value": result, "order": -1, "lost": -1, "grade": -1, "time_convertible": True}

    def calculate_aggregation(data: dict[str, Any], training: str, aggregation_type: str) -> dict[str, Any] | None:
        if aggregation_type not in aggregations_def.keys():
            return prepare_output(False, 0)

        agg_desc: AggregationDesc = aggregations_def[aggregation_type]
        result: int = 0
        if aggregation_type.startswith("intervals"):
            indexes: list[int] = [int(sec.split("/")[1]) for sec in agg_desc.inputs]
            ok, result = _sum_intervals(data, training, indexes)
        else:
            result = 0
            ok, inputs_data = _load_data(data, training, agg_desc.inputs, agg_desc.all_inputs_needed)
            if ok:
                inputs_data = agg_desc.apply_filters(inputs_data)
                result = agg_desc.apply_reducer(inputs_data)

        return prepare_output(ok, result)

    return calculate_aggregation
