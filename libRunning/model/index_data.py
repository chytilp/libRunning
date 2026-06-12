from dataclasses import dataclass

from libRunning.model.aggregation_desc import AggregationDesc


@dataclass
class IndexData:
    version: int
    files: list[str]
    aggregations: dict[str, AggregationDesc]
    sections: list[str]
    dashboard_sections: list[str]
    dashboard_aggregations: list[str]
