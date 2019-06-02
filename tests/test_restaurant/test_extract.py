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
        Headers.RESTAURANT_TYPES: ["Bakery", "Hamburgers", "American", "America", "Hamburgers"],
        Headers.BORO: ["BRONX", "BROOKLYN", "BROOKLYN", "BROOKLYN", "MANHATTAN"]
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


def test_extract_restaurant_contacts():
    csv = pd.DataFrame.from_dict({
        Headers.RESTAURANT_CODES: ["30075445", "30112340", "40356018", "40356018", "40061600"],
        Headers.BORO: ["BRONX", "BROOKLYN", "BROOKLYN", "BROOKLYN", "MANHATTAN"],
        Headers.BUILDING: [1007, 469, 2780, 2780, 335],
        Headers.STREET: ["MORRIS PARK AVE", "FLATBUSH AVENUE", "STILLWELL AVENUE", "STILLWELL AVENUE", "5 AVENUE"],
        Headers.ZIP_CODE: ["10462", "11225", "11224", "11224", "10016"],
        Headers.PHONE: ["7188924968", "7182875005", "7183723031", "7183723031", "7185554321"]
    })
    restaurants = extract._extract_restaurant_contacts(csv)
    expected_data = [
        {
            Headers.RESTAURANT_CODES: "30075445",
            Headers.BORO: "BRONX",
            Headers.BUILDING: 1007,
            Headers.STREET: "MORRIS PARK AVE",
            Headers.ZIP_CODE: "10462",
            Headers.PHONE: "7188924968"
        },
        {
            Headers.RESTAURANT_CODES: "30112340",
            Headers.BORO: "BROOKLYN",
            Headers.BUILDING: 469,
            Headers.STREET: "FLATBUSH AVENUE",
            Headers.ZIP_CODE: "11225",
            Headers.PHONE: "7182875005"
        },
        {
            Headers.RESTAURANT_CODES: "40356018",
            Headers.BORO: "BROOKLYN",
            Headers.BUILDING: 2780,
            Headers.STREET: "STILLWELL AVENUE",
            Headers.ZIP_CODE: "11224",
            Headers.PHONE: "7183723031"
        },
        {
            Headers.RESTAURANT_CODES: "40061600",
            Headers.BORO: "MANHATTAN",
            Headers.BUILDING: 335,
            Headers.STREET: "5 AVENUE",
            Headers.ZIP_CODE: "10016",
            Headers.PHONE: "7185554321"
        }
    ]
    assert restaurants == expected_data


def test_extract_restaurant_contacts__empty():
    csv = pd.DataFrame.from_dict({
        Headers.RESTAURANT_CODES: [],
        Headers.BORO: [],
        Headers.BUILDING: [],
        Headers.STREET: [],
        Headers.ZIP_CODE: [],
        Headers.PHONE: []})
    restaurants = extract._extract_restaurant_contacts(csv)
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
