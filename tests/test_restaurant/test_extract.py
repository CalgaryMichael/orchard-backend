import pandas as pd
from webapp.restaurant.etl import extract, Headers


def test_extract_restaurant_types():
    csv = pd.DataFrame.from_dict({Headers.RESTAURANT_TYPES.value: ["Hamburgers", "Bakery", "Hamburgers", "Thai", "thai"]})
    expected_data = ["Hamburgers", "Bakery", "Thai"]
    restaurant_types = extract.extract_restaurant_types(csv)
    assert list(restaurant_types) == expected_data


def test_extract_restaurant_types__empty():
    csv = pd.DataFrame.from_dict({Headers.RESTAURANT_TYPES.value: []})
    expected_data = []
    restaurant_types = extract.extract_restaurant_types(csv)
    assert list(restaurant_types) == expected_data


def test_extract_restaurants():
    csv = pd.DataFrame.from_dict({
        Headers.RESTAURANT_CODES.value: ["30075445", "30112340", "40356018", "40356018", "40361618"],
        Headers.RESTAURANT_NAME.value: ["MORRIS PARK BAKE SHOP", "WENDY'S", "RIVIERA CATERERS", "RIVIERA CATERERS", "WENDY'S"],
        Headers.RESTAURANT_TYPES.value: ["Bakery", "Hamburgers", "American", "America", "Hamburgers"],
        Headers.BORO.value: ["BRONX", "BROOKLYN", "BROOKLYN", "BROOKLYN", "MANHATTAN"]
    })
    restaurants = extract.extract_restaurants(csv)
    expected_data = [
        {
            Headers.RESTAURANT_CODES.value: "30075445",
            Headers.RESTAURANT_NAME.value: "MORRIS PARK BAKE SHOP",
            Headers.RESTAURANT_TYPES.value: "Bakery"
        },
        {
            Headers.RESTAURANT_CODES.value: "30112340",
            Headers.RESTAURANT_NAME.value: "WENDY'S",
            Headers.RESTAURANT_TYPES.value: "Hamburgers"
        },
        {
            Headers.RESTAURANT_CODES.value: "40356018",
            Headers.RESTAURANT_NAME.value: "RIVIERA CATERERS",
            Headers.RESTAURANT_TYPES.value: "American"
        },
        {
            Headers.RESTAURANT_CODES.value: "40361618",
            Headers.RESTAURANT_NAME.value: "WENDY'S",
            Headers.RESTAURANT_TYPES.value: "Hamburgers"
        }
    ]
    assert restaurants == expected_data


def test_extract_restaurants__empty():
    csv = pd.DataFrame.from_dict({
        Headers.RESTAURANT_CODES.value: [],
        Headers.RESTAURANT_NAME.value: [],
        Headers.RESTAURANT_TYPES.value: []
    })
    restaurants = extract.extract_restaurants(csv)
    expected_data = []
    assert restaurants == expected_data


def test_extract_restaurant_contacts():
    csv = pd.DataFrame.from_dict({
        Headers.RESTAURANT_CODES.value: ["30075445", "30112340", "40356018", "40356018", "40061600"],
        Headers.BORO.value: ["BRONX", "BROOKLYN", "BROOKLYN", "BROOKLYN", "MANHATTAN"],
        Headers.BUILDING.value: [1007, 469, 2780, 2780, 335],
        Headers.STREET.value: ["MORRIS PARK AVE", "FLATBUSH AVENUE", "STILLWELL AVENUE", "STILLWELL AVENUE", "5 AVENUE"],
        Headers.ZIP_CODE.value: ["10462", "11225", "11224", "11224", "10016"],
        Headers.PHONE.value: ["7188924968", "7182875005", "7183723031", "7183723031", "7185554321"]
    })
    restaurants = extract.extract_restaurant_contacts(csv)
    expected_data = [
        {
            Headers.RESTAURANT_CODES.value: "30075445",
            Headers.BORO.value: "BRONX",
            Headers.BUILDING.value: 1007,
            Headers.STREET.value: "MORRIS PARK AVE",
            Headers.ZIP_CODE.value: "10462",
            Headers.PHONE.value: "7188924968"
        },
        {
            Headers.RESTAURANT_CODES.value: "30112340",
            Headers.BORO.value: "BROOKLYN",
            Headers.BUILDING.value: 469,
            Headers.STREET.value: "FLATBUSH AVENUE",
            Headers.ZIP_CODE.value: "11225",
            Headers.PHONE.value: "7182875005"
        },
        {
            Headers.RESTAURANT_CODES.value: "40356018",
            Headers.BORO.value: "BROOKLYN",
            Headers.BUILDING.value: 2780,
            Headers.STREET.value: "STILLWELL AVENUE",
            Headers.ZIP_CODE.value: "11224",
            Headers.PHONE.value: "7183723031"
        },
        {
            Headers.RESTAURANT_CODES.value: "40061600",
            Headers.BORO.value: "MANHATTAN",
            Headers.BUILDING.value: 335,
            Headers.STREET.value: "5 AVENUE",
            Headers.ZIP_CODE.value: "10016",
            Headers.PHONE.value: "7185554321"
        }
    ]
    assert restaurants == expected_data


def test_extract_restaurant_contacts__empty():
    csv = pd.DataFrame.from_dict({
        Headers.RESTAURANT_CODES.value: [],
        Headers.BORO.value: [],
        Headers.BUILDING.value: [],
        Headers.STREET.value: [],
        Headers.ZIP_CODE.value: [],
        Headers.PHONE.value: []})
    restaurants = extract.extract_restaurant_contacts(csv)
    expected_data = []
    assert restaurants == expected_data


def test_extract_inspection_types():
    csv = pd.DataFrame.from_dict({Headers.INSPECTION_TYPE.value: [
        "Cycle Inspection / Initial Inspection",
        None,
        "Smoke-Free Air Act / Re-inspection"]})
    expected_data = [
        "Cycle Inspection / Initial Inspection",
        "Smoke-Free Air Act / Re-inspection"]
    inspection_types = extract.extract_inspection_types(csv)
    assert list(inspection_types) == expected_data


def test_extract_inspection_types__empty_list():
    csv = pd.DataFrame.from_dict({Headers.INSPECTION_TYPE.value: []})
    expected_data = []
    inspection_types = extract.extract_inspection_types(csv)
    assert list(inspection_types) == expected_data


def test_extract_inspections():
    csv = pd.DataFrame.from_dict({
        Headers.RESTAURANT_CODES.value: ["30075445", "30112340", "40356018", "40356018", "40061600"],
        Headers.INSPECTION_TYPE.value: ["Cycle Inspection / Initial Inspection"] * 5,
        Headers.INSPECTION_DATE.value: ["5/16/2019", "5/15/2019", "5/16/2019", "5/14/2019", "5/16/2019"],
        Headers.INSPECTION_SCORE.value: [18, 20, 14, 25, 5],
        Headers.GRADES.value: ["A", "B", None, "C", "A"],
        Headers.GRADE_DATE.value: ["5/16/2019", "5/15/2019", None, "5/14/2019", "5/16/2019"]
    })
    inspections = extract.extract_inspections(csv)
    expected_data = [
        {
            Headers.RESTAURANT_CODES.value: "30075445",
            Headers.INSPECTION_TYPE.value: "Cycle Inspection / Initial Inspection",
            Headers.INSPECTION_DATE.value: "5/16/2019",
            Headers.INSPECTION_SCORE.value: 18,
            Headers.GRADES.value: "A",
            Headers.GRADE_DATE.value: "5/16/2019"
        },
        {
            Headers.RESTAURANT_CODES.value: "30112340",
            Headers.INSPECTION_TYPE.value: "Cycle Inspection / Initial Inspection",
            Headers.INSPECTION_DATE.value: "5/15/2019",
            Headers.INSPECTION_SCORE.value: 20,
            Headers.GRADES.value: "B",
            Headers.GRADE_DATE.value: "5/15/2019"
        },
        {
            Headers.RESTAURANT_CODES.value: "40356018",
            Headers.INSPECTION_TYPE.value: "Cycle Inspection / Initial Inspection",
            Headers.INSPECTION_DATE.value: "5/16/2019",
            Headers.INSPECTION_SCORE.value: 14,
            Headers.GRADES.value: None,
            Headers.GRADE_DATE.value: None
        },
        {
            Headers.RESTAURANT_CODES.value: "40356018",
            Headers.INSPECTION_TYPE.value: "Cycle Inspection / Initial Inspection",
            Headers.INSPECTION_DATE.value: "5/14/2019",
            Headers.INSPECTION_SCORE.value: 25,
            Headers.GRADES.value: "C",
            Headers.GRADE_DATE.value: "5/14/2019"
        },
        {
            Headers.RESTAURANT_CODES.value: "40061600",
            Headers.INSPECTION_TYPE.value: "Cycle Inspection / Initial Inspection",
            Headers.INSPECTION_DATE.value: "5/16/2019",
            Headers.INSPECTION_SCORE.value: 5,
            Headers.GRADES.value: "A",
            Headers.GRADE_DATE.value: "5/16/2019"
        }
    ]
    assert inspections == expected_data


def test_extract_inspections__multiple_violations():
    csv = pd.DataFrame.from_dict({
        Headers.RESTAURANT_CODES.value: ["30075445", "30075445", "40356018", "40356018"],
        Headers.INSPECTION_TYPE.value: ["Cycle Inspection / Initial Inspection"] * 4,
        Headers.INSPECTION_DATE.value: ["5/16/2019", "5/15/2019", "5/16/2019", "5/16/2019"],
        Headers.INSPECTION_SCORE.value: [18, 20, 25, 25],
        Headers.GRADES.value: ["A", None, "C", "C"],
        Headers.GRADE_DATE.value: ["5/16/2019", None, "5/16/2019", "5/16/2019"],
        Headers.VIOLATION_CODE.value: ["04J", "08A", "10F", "06D"]
    })
    inspections = extract.extract_inspections(csv)
    expected_data = [
        {
            Headers.RESTAURANT_CODES.value: "30075445",
            Headers.INSPECTION_TYPE.value: "Cycle Inspection / Initial Inspection",
            Headers.INSPECTION_DATE.value: "5/16/2019",
            Headers.INSPECTION_SCORE.value: 18,
            Headers.GRADES.value: "A",
            Headers.GRADE_DATE.value: "5/16/2019"
        },
        {
            Headers.RESTAURANT_CODES.value: "30075445",
            Headers.INSPECTION_TYPE.value: "Cycle Inspection / Initial Inspection",
            Headers.INSPECTION_DATE.value: "5/15/2019",
            Headers.INSPECTION_SCORE.value: 20,
            Headers.GRADES.value: None,
            Headers.GRADE_DATE.value: None
        },
        {
            Headers.RESTAURANT_CODES.value: "40356018",
            Headers.INSPECTION_TYPE.value: "Cycle Inspection / Initial Inspection",
            Headers.INSPECTION_DATE.value: "5/16/2019",
            Headers.INSPECTION_SCORE.value: 25,
            Headers.GRADES.value: "C",
            Headers.GRADE_DATE.value: "5/16/2019"
        }
    ]
    assert inspections == expected_data


def test_extract_inspections__empty():
    csv = pd.DataFrame.from_dict({
        Headers.RESTAURANT_CODES.value: [],
        Headers.INSPECTION_TYPE.value: [],
        Headers.INSPECTION_DATE.value: [],
        Headers.INSPECTION_SCORE.value: [],
        Headers.GRADES.value: [],
        Headers.GRADE_DATE.value: []
    })
    inspections = extract.extract_inspections(csv)
    expected_data = []
    assert inspections == expected_data


def test_extract_grades():
    csv = pd.DataFrame.from_dict({Headers.GRADES.value: ["A", None, "", "B", "C", "", "G", "P", None, "Z"]})
    expected_data = ["A", "B", "C", "G", "P", "Z"]
    grades = extract.extract_grades(csv)
    assert list(grades) == expected_data


def test_extract_grades__empty():
    csv = pd.DataFrame.from_dict({Headers.GRADES.value: []})
    expected_data = []
    grades = extract.extract_grades(csv)
    assert list(grades) == expected_data


def test_extract_violations():
    violation_description = "Evidence of mice or live mice present in facility's food and/or non-food areas."
    csv = pd.DataFrame.from_dict({
        Headers.RESTAURANT_CODES.value: ["30075445", "30075445", "40356018", "40356018"],
        Headers.INSPECTION_DATE.value: ["5/16/2019", "5/15/2019", "5/16/2019", "5/16/2019"],
        Headers.VIOLATION_CODE.value: ["04J", "08A", "10F", "06D"],
        Headers.VIOLATION_DESCRIPTION.value: [violation_description] * 4,
        Headers.CRITICAL_RATING.value: ["Critical", "Critical", "Critical", "Not Critical"]
    })
    violations = extract.extract_violations(csv)
    expected_violations = [
        {
            Headers.RESTAURANT_CODES.value: "30075445",
            Headers.INSPECTION_DATE.value: "5/16/2019",
            Headers.VIOLATION_CODE.value: "04J",
            Headers.VIOLATION_DESCRIPTION.value: violation_description,
            Headers.CRITICAL_RATING.value: "Critical"
        },
        {
            Headers.RESTAURANT_CODES.value: "30075445",
            Headers.INSPECTION_DATE.value: "5/15/2019",
            Headers.VIOLATION_CODE.value: "08A",
            Headers.VIOLATION_DESCRIPTION.value: violation_description,
            Headers.CRITICAL_RATING.value: "Critical"
        },
        {
            Headers.RESTAURANT_CODES.value: "40356018",
            Headers.INSPECTION_DATE.value: "5/16/2019",
            Headers.VIOLATION_CODE.value: "10F",
            Headers.VIOLATION_DESCRIPTION.value: violation_description,
            Headers.CRITICAL_RATING.value: "Critical"
        },
        {
            Headers.RESTAURANT_CODES.value: "40356018",
            Headers.INSPECTION_DATE.value: "5/16/2019",
            Headers.VIOLATION_CODE.value: "06D",
            Headers.VIOLATION_DESCRIPTION.value: violation_description,
            Headers.CRITICAL_RATING.value: "Not Critical"
        }
    ]
    assert violations == expected_violations


def test_extract_violations__empty():
    violation_description = "Evidence of mice or live mice present in facility's food and/or non-food areas."
    csv = pd.DataFrame.from_dict({
        Headers.RESTAURANT_CODES.value: [],
        Headers.INSPECTION_DATE.value: [],
        Headers.VIOLATION_CODE.value: [],
        Headers.VIOLATION_DESCRIPTION.value: [],
        Headers.CRITICAL_RATING.value: []
    })
    violations = extract.extract_violations(csv)
    expected_violations = []
    assert violations == expected_violations
