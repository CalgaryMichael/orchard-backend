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
