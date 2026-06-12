import pytest

from libRunning.model.aggregation_desc import AggregationDesc, Filter


@pytest.mark.parametrize(
    "name, reducer, expected",
    (
        pytest.param("lenAggregation", "len", 3, id="len"),
        pytest.param("sumAggregation", "sum", 6, id="sum"),
    )
)
def test_aggregation_desc_wout_filters(name: str, reducer: str, expected: int) -> None:
    agg_desc = AggregationDesc(
        name=name,
        reducer=reducer,
    )
    values = [1, 2, 3]
    values = agg_desc.apply_filters(values)
    result: int = agg_desc.apply_reducer(values)
    assert result == expected


@pytest.mark.parametrize(
    "filters, name, reducer, expected",
    (
        pytest.param([Filter("==", 1)], "len==", "len", 1, id="(==,len)"),
        pytest.param([Filter("!=", 1)], "len!=", "len", 9, id="(!=,len)"),
        pytest.param([Filter(">", 3)], "len>", "len", 7, id="(>,len)"),
        pytest.param([Filter(">=", 3)], "len>=", "len", 8, id="(>=,len)"),
        pytest.param([Filter("<", 5)], "len<", "len", 4, id="(<,len)"),
        pytest.param([Filter("<=", 5)], "len<=", "len", 5, id="(<=,len)"),

        pytest.param([Filter("==", 1)], "sum==", "sum", 1, id="(==,sum)"),
        pytest.param([Filter("!=", 1)], "sum!=", "sum", 54, id="(!=,sum)"),
        pytest.param([Filter(">", 3)], "sum>", "sum", 49, id="(>,sum)"),
        pytest.param([Filter(">=", 3)], "sum>=", "sum", 52, id="(>=,sum)"),
        pytest.param([Filter("<", 5)], "sum<", "sum", 10, id="(<,sum)"),
        pytest.param([Filter("<=", 5)], "sum<=", "sum", 15, id="(<=,sum)"),

        pytest.param([Filter("==", 1)], "min==", "min", 1, id="(==,min)"),
        pytest.param([Filter("!=", 1)], "min!=", "min", 2, id="(!=,min)"),
        pytest.param([Filter(">", 3)], "min>", "min", 4, id="(>,min)"),
        pytest.param([Filter(">=", 3)], "min>=", "min", 3, id="(>=,min)"),
        pytest.param([Filter("<", 5)], "min<", "min", 1, id="(<,min)"),
        pytest.param([Filter("<=", 5)], "min<=", "min", 1, id="(<=,min)"),

        pytest.param([Filter("==", 1)], "max==", "max", 1, id="(==,max)"),
        pytest.param([Filter("!=", 1)], "max!=", "max", 10, id="(!=,max)"),
        pytest.param([Filter(">", 3)], "max>", "max", 10, id="(>,max)"),
        pytest.param([Filter(">=", 3)], "max>=", "max", 10, id="(>=,max)"),
        pytest.param([Filter("<", 5)], "max<", "max", 4, id="(<,max)"),
        pytest.param([Filter("<=", 5)], "max<=", "max", 5, id="(<=,max)"),

        pytest.param([Filter("==", 1)], "avg==", "avg", 1, id="(==,avg)"),
        pytest.param([Filter("!=", 1)], "avg!=", "avg", 6, id="(!=,avg)"),
        pytest.param([Filter(">", 3)], "avg>", "avg", 7, id="(>,avg)"),
        pytest.param([Filter(">=", 3)], "avg>=", "avg", 7, id="(>=,avg)"),
        pytest.param([Filter("<", 5)], "avg<", "avg", 3, id="(<,avg)"),
        pytest.param([Filter("<=", 5)], "avg<=", "avg", 3, id="(<=,avg)"),
    )
)
def test_aggregation_desc_with_filters(filters: list[Filter], name: str, reducer: str, expected: int) -> None:
    values: list[int] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    agg_desc = AggregationDesc(
        reducer=reducer,
        filters=filters,
        name=name,
    )
    values = agg_desc.apply_filters(values)
    result: int = agg_desc.apply_reducer(values)
    assert result == expected
