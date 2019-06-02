import datetime
import pytest
from webapp.restaurant import choices, models
from webapp.restaurant.etl import load
from . import utils


@pytest.mark.django_db
def test_load_restaurant_types():
    assert models.RestaurantType.objects.all().count() == 0
    unloaded = [
        models.RestaurantType(slug="hamburgers", description="Hamburgers"),
        models.RestaurantType(slug="thai", description="Thai"),
        models.RestaurantType(slug="bakery", description="Bakery")]
    load.load_restaurant_types(unloaded)
    assert models.RestaurantType.objects.all().count() == 3


@pytest.mark.django_db
def test_load_restaurant_types__empty_list():
    assert models.RestaurantType.objects.all().count() == 0
    unloaded = []
    load.load_restaurant_types(unloaded)
    assert models.RestaurantType.objects.all().count() == 0


@pytest.mark.django_db
def test_load_restaurants():
    bakery = utils.create_restaurant_type("bakery")
    hamburgers = utils.create_restaurant_type("hamburgers")
    american = utils.create_restaurant_type("american")

    assert models.Restaurant.objects.all().count() == 0
    unloaded = [
        models.Restaurant(code="30075445", name="MORRIS PARK BAKE SHOP", restaurant_type_id=bakery.id),
        models.Restaurant(code="30112340", name="WENDY'S", restaurant_type_id=hamburgers.id),
        models.Restaurant(code="40356018", name="RIVIERA CATERERS", restaurant_type_id=american.id)]
    load.load_restaurants(iter(unloaded))
    assert models.Restaurant.objects.all().count() == 3
    assert models.Restaurant.objects.filter(restaurant_type=bakery).count() == 1
    assert models.Restaurant.objects.filter(restaurant_type=hamburgers).count() == 1
    assert models.Restaurant.objects.filter(restaurant_type=american).count() == 1


@pytest.mark.django_db
def test_load_restaurants__empty_list():
    assert models.Restaurant.objects.all().count() == 0
    unloaded = []
    load.load_restaurants(unloaded)
    assert models.Restaurant.objects.all().count() == 0


@pytest.mark.django_db
def test_load_restaurant_contacts():
    morris = utils.create_restaurant("30075445", "MORRIS PARK BAKE SHOP", "bakery")
    wendys = utils.create_restaurant("30112340", "WENDY'S", "hamburgers")
    riviera = utils.create_restaurant("40356018", "RIVIERA CATERERS", "american")

    assert models.RestaurantContact.objects.all().count() == 0
    unloaded = [
        models.RestaurantContact(
            restaurant_id=morris.id,
            boro="BRONX",
            building_number=1007,
            street="MORRIS PARK AVE",
            zip_code="10462",
            phone="7188924968"),
        models.RestaurantContact(
            restaurant_id=wendys.id,
            boro="BROOKLYN",
            building_number=469,
            street="FLATBUSH AVENUE",
            zip_code="11225",
            phone="7182875005"),
        models.RestaurantContact(
            restaurant_id=riviera.id,
            boro="BROOKLYN",
            building_number=2780,
            street="STILLWELL AVENUE",
            zip_code="11224",
            phone="7183723031")]
    load.load_restaurant_contacts(iter(unloaded))
    assert models.RestaurantContact.objects.all().count() == 3
    assert models.RestaurantContact.objects.filter(restaurant=morris).count() == 1
    assert models.RestaurantContact.objects.filter(restaurant=wendys).count() == 1
    assert models.RestaurantContact.objects.filter(restaurant=riviera).count() == 1


@pytest.mark.django_db
def test_load_restaurant_contacts__empty_list():
    assert models.RestaurantContact.objects.all().count() == 0
    unloaded = []
    load.load_restaurant_contacts(unloaded)
    assert models.RestaurantContact.objects.all().count() == 0


@pytest.mark.django_db
def test_load_grades():
    assert models.Grade.objects.all().count() == 0
    unloaded = [
        models.Grade(slug="a", label="A"),
        models.Grade(slug="b", label="B"),
        models.Grade(slug="c", label="C")]
    load.load_grades(unloaded)
    assert models.Grade.objects.all().count() == 3


@pytest.mark.django_db
def test_load_grades__empty_list():
    assert models.Grade.objects.all().count() == 0
    unloaded = []
    load.load_grades(unloaded)
    assert models.Grade.objects.all().count() == 0


@pytest.mark.django_db
def test_load_inspection_types():
    assert models.InspectionType.objects.all().count() == 0
    unloaded = [
        models.InspectionType(
            slug="cycle-inspection-initial-inspection",
            description="Cycle Inspection / Initial Inspection"),
        models.InspectionType(
            slug="smoke-free-air-act-re-inspection",
            description="Smoke-Free Air Act / Re-inspection")]
    load.load_inspection_types(unloaded)
    assert models.InspectionType.objects.all().count() == 2


@pytest.mark.django_db
def test_load_inspection_types__empty_list():
    assert models.InspectionType.objects.all().count() == 0
    unloaded = []
    load.load_inspection_types(unloaded)
    assert models.InspectionType.objects.all().count() == 0


@pytest.mark.django_db
def test_load_inspections():
    inspection_type = utils.create_inspection_type("Cycle Inspection / Initial Inspection")

    morris = utils.create_restaurant("30075445", "MORRIS PARK BAKE SHOP", "bakery")
    wendys1 = utils.create_restaurant("30112340", "WENDY'S", "hamburgers")
    riviera = utils.create_restaurant("40356018", "RIVIERA CATERERS", "american")
    wendys2 = utils.create_restaurant("40061600", "WENDY'S", "hamburgers")

    grade_a = utils.create_grade("A")
    grade_b = utils.create_grade("B")
    grade_c = utils.create_grade("C")

    assert models.Inspection.objects.all().count() == 0
    unloaded = [
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
            grade_date=datetime.date(2019, 5, 16))]
    load.load_inspections(iter(unloaded))
    assert models.Inspection.objects.all().count() == 5
    assert models.Inspection.objects.filter(inspection_type=inspection_type).count() == 5
    assert models.Inspection.objects.filter(restaurant=morris).count() == 1
    assert models.Inspection.objects.filter(restaurant=wendys1).count() == 1
    assert models.Inspection.objects.filter(restaurant=riviera).count() == 2
    assert models.Inspection.objects.filter(restaurant=wendys2).count() == 1
    assert models.Inspection.objects.filter(grade=grade_a).count() == 2
    assert models.Inspection.objects.filter(grade=grade_b).count() == 1
    assert models.Inspection.objects.filter(grade=grade_c).count() == 1
    assert models.Inspection.objects.filter(grade=None).count() == 1


@pytest.mark.django_db
def test_load_inspections__empty_list():
    assert models.Inspection.objects.all().count() == 0
    unloaded = []
    load.load_inspections(unloaded)
    assert models.Inspection.objects.all().count() == 0


@pytest.mark.django_db
def test_load_violations():
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

    unloaded = [
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
    load.load_violations(unloaded)
    assert models.Violation.objects.all().count() == 4
    assert models.Violation.objects.filter(inspection=inspect1).count() == 1
    assert models.Violation.objects.filter(inspection=inspect2).count() == 1
    assert models.Violation.objects.filter(inspection=inspect3).count() == 2
