from libRunning.model.grade import Grade


def test_grade_object() -> None:
    g = Grade(grade=1, from_=100, to_=105)
    assert g.reverse is False
    assert g.match(99) is False
    assert g.match(100) is True
    assert g.match(101) is True
    assert g.match(102) is True
    assert g.match(103) is True
    assert g.match(104) is True
    assert g.match(105) is False
    assert g.match(106) is False


def test_grade_object_reverse() -> None:
    g = Grade(grade=1, from_=105, to_=100)
    assert g.reverse is True
    assert g.match(106) is False
    assert g.match(105) is True
    assert g.match(104) is True
    assert g.match(103) is True
    assert g.match(102) is True
    assert g.match(101) is True
    assert g.match(100) is False
    assert g.match(99) is False
