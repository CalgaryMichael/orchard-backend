import pandas as pd
from webapp.restaurant.etl import extract, Headers


def test_extract_restaurant_types():
    csv = pd.DataFrame.from_dict({Headers.RESTAURANT_TYPES: ["Hamburgers", "Bakery", "Hamburgers", "Thai", "thai"]})
    expected_data = ["Hamburgers", "Bakery", "Thai"]
    restaurant_types = extract._extract_restaurant_types(csv)
    assert list(restaurant_types) == expected_data


def test_extract_restaurant_types__empty():
    csv = pd.DataFrame.from_dict({Headers.RESTAURANT_TYPES: []})
    expected_data = []
    restaurant_types = extract._extract_restaurant_types(csv)
    assert list(restaurant_types) == expected_data


def test_extract_restaurants():
    csv = pd.DataFrame.from_dict({
        Headers.RESTAURANT_CODES: ["30075445", "30112340", "40356018", "40356018", "40361618"],
        Headers.RESTAURANT_NAME: ["MORRIS PARK BAKE SHOP", "WENDY'S", "RIVIERA CATERERS", "RIVIERA CATERERS", "WENDY'S"],
        Headers.RESTAURANT_TYPES: ["Bakery", "Hamburgers", "American", "America", "Hamburgers"]
    })
    restaurants = extract._extract_restaurants(csv)
    expected_data = [
        {
            Headers.RESTAURANT_CODES: "30075445",
            Headers.RESTAURANT_NAME: "MORRIS PARK BAKE SHOP",
            Headers.RESTAURANT_TYPES: "Bakery"
        },
        {
            Headers.RESTAURANT_CODES: "30112340",
            Headers.RESTAURANT_NAME: "WENDY'S",
            Headers.RESTAURANT_TYPES: "Hamburgers"
        },
        {
            Headers.RESTAURANT_CODES: "40356018",
            Headers.RESTAURANT_NAME: "RIVIERA CATERERS",
            Headers.RESTAURANT_TYPES: "American"
        },
        {
            Headers.RESTAURANT_CODES: "40361618",
            Headers.RESTAURANT_NAME: "WENDY'S",
            Headers.RESTAURANT_TYPES: "Hamburgers"
        }
    ]
    assert restaurants == expected_data


def test_extract_restaurants__empty():
    csv = pd.DataFrame.from_dict({
        Headers.RESTAURANT_CODES: [],
        Headers.RESTAURANT_NAME: [],
        Headers.RESTAURANT_TYPES: []
    })
    restaurants = extract._extract_restaurants(csv)
    expected_data = []
    assert restaurants == expected_data


def test_extract_grades():
    csv = pd.DataFrame.from_dict({Headers.GRADES: ["A", None, "", "B", "C", "", "G", "P", None, "Z"]})
    expected_data = ["A", "B", "C", "G", "P", "Z"]
    grades = extract._extract_grades(csv)
    assert list(grades) == expected_data


def test_extract_grades__empty():
    csv = pd.DataFrame.from_dict({Headers.GRADES: []})
    expected_data = []
    grades = extract._extract_grades(csv)
    assert list(grades) == expected_data
