from webapp.restaurant import choices


def test_choices():
    class TestEnum(choices.ChoiceEnum):
        A = 0
        B = 1

    expected_choices = [(0, "A"), (1, "B")]
    assert TestEnum.choices() == expected_choices
