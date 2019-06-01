from webapp.restaurant.etl import transform
from webapp.restaurant import models


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
