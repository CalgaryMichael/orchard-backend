import pytest
from webapp.restaurant import models
from webapp.restaurant.etl import load


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
