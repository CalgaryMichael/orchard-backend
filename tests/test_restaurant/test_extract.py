import pandas as pd
from webapp.restaurant.etl import extract


def test_extract_restaurant_types():
    csv = pd.DataFrame.from_dict({extract.RESTAURANT_TYPES: ["Hamburgers", "Bakery", "Hamburgers", "Thai", "thai"]})
    expected_data = ["Hamburgers", "Bakery", "Thai"]
    restaurant_types = extract._extract_restaurant_types(csv)
    assert list(restaurant_types) == expected_data


def test_extract_restaurant_types__empty():
    csv = pd.DataFrame.from_dict({extract.RESTAURANT_TYPES: []})
    expected_data = []
    restaurant_types = extract._extract_restaurant_types(csv)
    assert list(restaurant_types) == expected_data
