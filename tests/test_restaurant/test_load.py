import pytest
from webapp.restaurant import models
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
