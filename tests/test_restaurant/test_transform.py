import datetime
import pytest
from webapp.restaurant import models
from webapp.restaurant.etl import transform, Headers
from . import utils


def test_transform_restaurant_types():
    untransformed = ["Hamburgers", "Thai", "Bakery"]
    restaurant_types = transform._transform_restaurant_types(untransformed)
    expected_types = [
        models.RestaurantType(slug="hamburgers", description="Hamburgers"),
        models.RestaurantType(slug="thai", description="Thai"),
        models.RestaurantType(slug="bakery", description="Bakery")]
    for i, restaurant_type in enumerate(restaurant_types):
        assert restaurant_type.slug == expected_types[i].slug
        assert restaurant_type.description == expected_types[i].description


@pytest.mark.django_db
def test_transform_restaurants():
    utils.create_restaurant_type("bakery")
    utils.create_restaurant_type("hamburgers")
    utils.create_restaurant_type("american")

    untransformed = [
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
    restaurants = transform._transform_restaurants(untransformed)
    expected_restaurants = [
        models.Restaurant(code="30075445", name="MORRIS PARK BAKE SHOP", restaurant_type_id=1),
        models.Restaurant(code="30112340", name="WENDY'S", restaurant_type_id=2),
        models.Restaurant(code="40356018", name="RIVIERA CATERERS", restaurant_type_id=3),
        models.Restaurant(code="40361618", name="WENDY'S", restaurant_type_id=2)]
    for i, restaurant in enumerate(restaurants):
        assert restaurant.code == expected_restaurants[i].code
        assert restaurant.name == expected_restaurants[i].name
        assert restaurant.restaurant_type_id == expected_restaurants[i].restaurant_type_id


@pytest.mark.django_db
def test_transform_restaurant_contacts():
    utils.create_restaurant("30075445", "MORRIS PARK BAKE SHOP", "bakery")
    utils.create_restaurant("30112340", "WENDY'S", "hamburgers")
    utils.create_restaurant("40356018", "RIVIERA CATERERS", "american")
    utils.create_restaurant("40061600", "WENDY'S", "hamburgers")

    untransformed = [
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
    restaurant_contacts = transform._transform_restaurant_contacts(untransformed)
    expected_contacts = [
        models.RestaurantContact(
            restaurant_id=1,
            boro="BRONX",
            building_number=1007,
            street="MORRIS PARK AVE",
            zip_code="10462",
            phone="7188924968"),
        models.RestaurantContact(
            restaurant_id=2,
            boro="BROOKLYN",
            building_number=469,
            street="FLATBUSH AVENUE",
            zip_code="11225",
            phone="7182875005"),
        models.RestaurantContact(
            restaurant_id=3,
            boro="BROOKLYN",
            building_number=2780,
            street="STILLWELL AVENUE",
            zip_code="11224",
            phone="7183723031"),
        models.RestaurantContact(
            restaurant_id=4,
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
    grades = transform._transform_grades(untransformed)
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


@pytest.mark.django_db
def test_transform_inspections():
    morris = utils.create_restaurant("30075445", "MORRIS PARK BAKE SHOP", "bakery")
    wendys1 = utils.create_restaurant("30112340", "WENDY'S", "hamburgers")
    riviera = utils.create_restaurant("40356018", "RIVIERA CATERERS", "american")
    wendys2 = utils.create_restaurant("40061600", "WENDY'S", "hamburgers")

    grade_a = utils.create_grade("A")
    grade_b = utils.create_grade("B")
    grade_c = utils.create_grade("C")

    untransformed = [
        {
            Headers.RESTAURANT_CODES: "30075445",
            Headers.INSPECTION_TYPE: "Cycle Inspection / Initial Inspection",
            Headers.INSPECTION_DATE: "5/16/2019",
            Headers.INSPECTION_SCORE: 18,
            Headers.GRADES: "A",
            Headers.GRADE_DATE: "5/16/2019"
        },
        {
            Headers.RESTAURANT_CODES: "30112340",
            Headers.INSPECTION_TYPE: "Cycle Inspection / Initial Inspection",
            Headers.INSPECTION_DATE: "5/15/2019",
            Headers.INSPECTION_SCORE: 20,
            Headers.GRADES: "B",
            Headers.GRADE_DATE: "5/15/2019"
        },
        {
            Headers.RESTAURANT_CODES: "40356018",
            Headers.INSPECTION_TYPE: "Cycle Inspection / Initial Inspection",
            Headers.INSPECTION_DATE: "5/16/2019",
            Headers.INSPECTION_SCORE: 14,
            Headers.GRADES: None,
            Headers.GRADE_DATE: None
        },
        {
            Headers.RESTAURANT_CODES: "40356018",
            Headers.INSPECTION_TYPE: "Cycle Inspection / Initial Inspection",
            Headers.INSPECTION_DATE: "5/14/2019",
            Headers.INSPECTION_SCORE: 25,
            Headers.GRADES: "C",
            Headers.GRADE_DATE: "5/14/2019"
        },
        {
            Headers.RESTAURANT_CODES: "40061600",
            Headers.INSPECTION_TYPE: "Cycle Inspection / Initial Inspection",
            Headers.INSPECTION_DATE: "5/16/2019",
            Headers.INSPECTION_SCORE: 5,
            Headers.GRADES: "A",
            Headers.GRADE_DATE: "5/16/2019"
        }
    ]
    inspections = transform._transform_inspections(untransformed)
    expected_inspections = [
        models.Inspection(
            restaurant_id=morris.id,
            inspection_type="Cycle Inspection / Initial Inspection",
            inspection_date=datetime.date(2019, 5, 16),
            score=18,
            grade_id=grade_a.id,
            grade_date=datetime.date(2019, 5, 16)),
        models.Inspection(
            restaurant_id=wendys1.id,
            inspection_type="Cycle Inspection / Initial Inspection",
            inspection_date=datetime.date(2019, 5, 15),
            score=20,
            grade_id=grade_b.id,
            grade_date=datetime.date(2019, 5, 15)),
        models.Inspection(
            restaurant_id=riviera.id,
            inspection_type="Cycle Inspection / Initial Inspection",
            inspection_date=datetime.date(2019, 5, 16),
            score=14,
            grade_id=None,
            grade_date=None),
        models.Inspection(
            restaurant_id=riviera.id,
            inspection_type="Cycle Inspection / Initial Inspection",
            inspection_date=datetime.date(2019, 5, 14),
            score=25,
            grade_id=grade_c.id,
            grade_date=datetime.date(2019, 5, 14)),
        models.Inspection(
            restaurant_id=wendys2.id,
            inspection_type="Cycle Inspection / Initial Inspection",
            inspection_date=datetime.date(2019, 5, 16),
            score=5,
            grade_id=grade_a.id,
            grade_date=datetime.date(2019, 5, 16))
        ]
    for i, inspection in enumerate(inspections):
        assert inspection.restaurant_id == expected_inspections[i].restaurant_id
        assert inspection.inspection_type == expected_inspections[i].inspection_type
        assert inspection.inspection_date == expected_inspections[i].inspection_date
        assert inspection.score == expected_inspections[i].score
        assert inspection.grade_id == expected_inspections[i].grade_id
        assert inspection.grade_date == expected_inspections[i].grade_date
