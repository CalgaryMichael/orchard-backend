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
