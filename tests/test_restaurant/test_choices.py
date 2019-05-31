from webapp.restaurant import choices


def test_choices():
    class TestEnum(choices.ChoiceEnum):
        A = 0
        B = 1

    expected_choices = [(0, "A"), (1, "B")]
    assert TestEnum.choices() == expected_choices


def test_as_string():
    class TestEnum(choices.ChoiceEnum):
        A = 0
        B = "jazz"

    assert str(TestEnum.A) == "0"
    assert repr(TestEnum.A) == "0"
    assert str(TestEnum.B) == "jazz"
    assert repr(TestEnum.B) == "jazz"
