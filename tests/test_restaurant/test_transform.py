import datetime
import pytest
from webapp.restaurant import choices, models
from webapp.restaurant.etl import transform, Headers
from . import utils


def test_transform_restaurant_types():
    untransformed = ["Hamburgers", "Thai", "Bakery"]
    restaurant_types = transform.transform_restaurant_types(untransformed)
    expected_types = [
        models.RestaurantType(slug="hamburgers", description="Hamburgers"),
        models.RestaurantType(slug="thai", description="Thai"),
        models.RestaurantType(slug="bakery", description="Bakery")]
    for i, restaurant_type in enumerate(restaurant_types):
        assert restaurant_type.slug == expected_types[i].slug
        assert restaurant_type.description == expected_types[i].description


@pytest.mark.django_db
def test_transform_restaurants():
    bakery = utils.create_restaurant_type("bakery")
    hamburgers = utils.create_restaurant_type("hamburgers")
    american = utils.create_restaurant_type("american")

    untransformed = [
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
    restaurants = transform.transform_restaurants(untransformed)
    expected_restaurants = [
        models.Restaurant(code="30075445", name="MORRIS PARK BAKE SHOP", restaurant_type_id=bakery.id),
        models.Restaurant(code="30112340", name="WENDY'S", restaurant_type_id=hamburgers.id),
        models.Restaurant(code="40356018", name="RIVIERA CATERERS", restaurant_type_id=american.id),
        models.Restaurant(code="40361618", name="WENDY'S", restaurant_type_id=hamburgers.id)]
    for i, restaurant in enumerate(restaurants):
        assert restaurant.code == expected_restaurants[i].code
        assert restaurant.name == expected_restaurants[i].name
        assert restaurant.restaurant_type_id == expected_restaurants[i].restaurant_type_id


@pytest.mark.django_db
def test_transform_restaurant_contacts():
    restaurant1 = utils.create_restaurant("30075445", "MORRIS PARK BAKE SHOP", "bakery")
    restaurant2 = utils.create_restaurant("30112340", "WENDY'S", "hamburgers")
    restaurant3 = utils.create_restaurant("40356018", "RIVIERA CATERERS", "american")
    restaurant4 = utils.create_restaurant("40061600", "WENDY'S", "hamburgers")

    untransformed = [
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
    restaurant_contacts = transform.transform_restaurant_contacts(untransformed)
    expected_contacts = [
        models.RestaurantContact(
            restaurant_id=restaurant1.id,
            boro="BRONX",
            building_number=1007,
            street="MORRIS PARK AVE",
            zip_code="10462",
            phone="7188924968"),
        models.RestaurantContact(
            restaurant_id=restaurant2.id,
            boro="BROOKLYN",
            building_number=469,
            street="FLATBUSH AVENUE",
            zip_code="11225",
            phone="7182875005"),
        models.RestaurantContact(
            restaurant_id=restaurant3.id,
            boro="BROOKLYN",
            building_number=2780,
            street="STILLWELL AVENUE",
            zip_code="11224",
            phone="7183723031"),
        models.RestaurantContact(
            restaurant_id=restaurant4.id,
            boro="MANHATTAN",
            building_number=335,
            street="5 AVENUE",
            zip_code="10016",
            phone="7185554321")]
    for i, contact in enumerate(restaurant_contacts):
        assert contact.boro == expected_contacts[i].boro
        assert contact.building_number == expected_contacts[i].building_number
        assert contact.street == expected_contacts[i].street
        assert contact.zip_code == expected_contacts[i].zip_code
        assert contact.phone == expected_contacts[i].phone
        assert contact.restaurant_id == expected_contacts[i].restaurant_id


def test_transform_grades():
    untransformed = ["A", "B", "C", "P", "G", "Z"]
    grades = transform.transform_grades(untransformed)
    expected_grades = [
        models.Grade(slug="a", label="A"),
        models.Grade(slug="b", label="B"),
        models.Grade(slug="c", label="C"),
        models.Grade(slug="p", label="P"),
        models.Grade(slug="g", label="G"),
        models.Grade(slug="z", label="Z")]
    for i, grade in enumerate(grades):
        assert grade.slug == expected_grades[i].slug
        assert grade.label == expected_grades[i].label


def test_transform_inspection_types():
    untransformed = [
        "Cycle Inspection / Initial Inspection",
        "Smoke-Free Air Act / Re-inspection"]
    inspection_types = transform.transform_inspection_types(untransformed)
    expected_types = [
        models.InspectionType(
            slug="cycle-inspection-initial-inspection",
            description="Cycle Inspection / Initial Inspection"),
        models.InspectionType(
            slug="smoke-free-air-act-re-inspection",
            description="Smoke-Free Air Act / Re-inspection")]
    for i, inspection_type in enumerate(inspection_types):
        assert inspection_type.slug == expected_types[i].slug
        assert inspection_type.description == expected_types[i].description


@pytest.mark.django_db
def test_transform_inspections():
    inspection_type = utils.create_inspection_type("Cycle Inspection / Initial Inspection")

    morris = utils.create_restaurant("30075445", "MORRIS PARK BAKE SHOP", "bakery")
    wendys1 = utils.create_restaurant("30112340", "WENDY'S", "hamburgers")
    riviera = utils.create_restaurant("40356018", "RIVIERA CATERERS", "american")
    wendys2 = utils.create_restaurant("40061600", "WENDY'S", "hamburgers")

    grade_a = utils.create_grade("A")
    grade_b = utils.create_grade("B")
    grade_c = utils.create_grade("C")

    untransformed = [
        {
            Headers.RESTAURANT_CODES.value: "30075445",
            Headers.INSPECTION_TYPE.value: "Cycle Inspection / Initial Inspection",
            Headers.INSPECTION_DATE.value: "5/16/19",
            Headers.INSPECTION_SCORE.value: 18,
            Headers.GRADES.value: "A",
            Headers.GRADE_DATE.value: "5/16/19"
        },
        {
            Headers.RESTAURANT_CODES.value: "30112340",
            Headers.INSPECTION_TYPE.value: "Cycle Inspection / Initial Inspection",
            Headers.INSPECTION_DATE.value: "5/15/19",
            Headers.INSPECTION_SCORE.value: 20,
            Headers.GRADES.value: "B",
            Headers.GRADE_DATE.value: "5/15/19"
        },
        {
            Headers.RESTAURANT_CODES.value: "40356018",
            Headers.INSPECTION_TYPE.value: "Cycle Inspection / Initial Inspection",
            Headers.INSPECTION_DATE.value: "5/16/19",
            Headers.INSPECTION_SCORE.value: 14,
            Headers.GRADES.value: None,
            Headers.GRADE_DATE.value: None
        },
        {
            Headers.RESTAURANT_CODES.value: "40356018",
            Headers.INSPECTION_TYPE.value: "Cycle Inspection / Initial Inspection",
            Headers.INSPECTION_DATE.value: "5/14/19",
            Headers.INSPECTION_SCORE.value: 25,
            Headers.GRADES.value: "C",
            Headers.GRADE_DATE.value: "5/14/19"
        },
        {
            Headers.RESTAURANT_CODES.value: "40061600",
            Headers.INSPECTION_TYPE.value: "Cycle Inspection / Initial Inspection",
            Headers.INSPECTION_DATE.value: "5/16/19",
            Headers.INSPECTION_SCORE.value: 5,
            Headers.GRADES.value: "A",
            Headers.GRADE_DATE.value: "5/16/19"
        }
    ]
    inspections = transform.transform_inspections(untransformed)
    expected_inspections = [
        models.Inspection(
            restaurant_id=morris.id,
            inspection_type_id=inspection_type.id,
            inspection_date=datetime.date(2019, 5, 16),
            score=18,
            grade_id=grade_a.id,
            grade_date=datetime.date(2019, 5, 16)),
        models.Inspection(
            restaurant_id=wendys1.id,
            inspection_type_id=inspection_type.id,
            inspection_date=datetime.date(2019, 5, 15),
            score=20,
            grade_id=grade_b.id,
            grade_date=datetime.date(2019, 5, 15)),
        models.Inspection(
            restaurant_id=riviera.id,
            inspection_type_id=inspection_type.id,
            inspection_date=datetime.date(2019, 5, 16),
            score=14,
            grade_id=None,
            grade_date=None),
        models.Inspection(
            restaurant_id=riviera.id,
            inspection_type_id=inspection_type.id,
            inspection_date=datetime.date(2019, 5, 14),
            score=25,
            grade_id=grade_c.id,
            grade_date=datetime.date(2019, 5, 14)),
        models.Inspection(
            restaurant_id=wendys2.id,
            inspection_type_id=inspection_type.id,
            inspection_date=datetime.date(2019, 5, 16),
            score=5,
            grade_id=grade_a.id,
            grade_date=datetime.date(2019, 5, 16))
        ]
    for i, inspection in enumerate(inspections):
        assert inspection.restaurant_id == expected_inspections[i].restaurant_id
        assert inspection.inspection_type_id == expected_inspections[i].inspection_type_id
        assert inspection.inspection_date == expected_inspections[i].inspection_date
        assert inspection.score == expected_inspections[i].score
        assert inspection.grade_id == expected_inspections[i].grade_id
        assert inspection.grade_date == expected_inspections[i].grade_date


@pytest.mark.django_db
def test_transform_violations():
    description = "Evidence of mice or live mice present in facility's food and/or non-food areas."
    restaurant1 = utils.create_restaurant(code="30075445", name="WENDY'S", type_slug="hamburgers")
    restaurant2 = utils.create_restaurant(code="40356018", name="RIVIERA CATERING", type_slug="american")
    inspect1 = utils.create_inspection(
        restaurant=restaurant1,
        inspection_type="Cycle Inspection / Initial Inspection",
        date="2019-05-16",
        score=14)
    inspect2 = utils.create_inspection(
        restaurant=restaurant1,
        inspection_type="Cycle Inspection / Initial Inspection",
        date="2019-05-15",
        score=20)
    inspect3 = utils.create_inspection(
        restaurant=restaurant2,
        inspection_type="Cycle Inspection / Initial Inspection",
        date="2019-05-16",
        score=25)
    untransformed = [
        {
            Headers.RESTAURANT_CODES.value: "30075445",
            Headers.INSPECTION_DATE.value: "5/16/19",
            Headers.VIOLATION_CODE.value: "04J",
            Headers.VIOLATION_DESCRIPTION.value: description,
            Headers.CRITICAL_RATING.value: "Critical"
        },
        {
            Headers.RESTAURANT_CODES.value: "30075445",
            Headers.INSPECTION_DATE.value: "5/15/19",
            Headers.VIOLATION_CODE.value: "08A",
            Headers.VIOLATION_DESCRIPTION.value: description,
            Headers.CRITICAL_RATING.value: "Not Applicable"
        },
        {
            Headers.RESTAURANT_CODES.value: "40356018",
            Headers.INSPECTION_DATE.value: "5/16/19",
            Headers.VIOLATION_CODE.value: "10F",
            Headers.VIOLATION_DESCRIPTION.value: description,
            Headers.CRITICAL_RATING.value: "Critical"
        },
        {
            Headers.RESTAURANT_CODES.value: "40356018",
            Headers.INSPECTION_DATE.value: "5/16/19",
            Headers.VIOLATION_CODE.value: "06D",
            Headers.VIOLATION_DESCRIPTION.value: description,
            Headers.CRITICAL_RATING.value: "Not Critical"
        }
    ]
    violations = transform.transform_violations(untransformed)
    expected_violations = [
        models.Violation(
            inspection_id=inspect1.id,
            code="04J",
            description=description,
            critical_rating=choices.CriticalRating.CRITICAL.value),
        models.Violation(
            inspection_id=inspect2.id,
            code="08A",
            description=description,
            critical_rating=choices.CriticalRating.NOT_APPLICABLE.value),
        models.Violation(
            inspection_id=inspect3.id,
            code="10F",
            description=description,
            critical_rating=choices.CriticalRating.CRITICAL.value),
        models.Violation(
            inspection_id=inspect3.id,
            code="06D",
            description=description,
            critical_rating=choices.CriticalRating.NOT_CRITICAL.value)
    ]
    for i, violation in enumerate(violations):
        assert violation.inspection_id == expected_violations[i].inspection_id
        assert violation.code == expected_violations[i].code
        assert violation.critical_rating == expected_violations[i].critical_rating
        assert violation.description == expected_violations[i].description
