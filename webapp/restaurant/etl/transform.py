from webapp.restaurant import models
from django.utils.text import slugify


def _transform_restaurant_types(type_list):
    """Returns a generator of a normalized RestaurantType object"""
    return (models.RestaurantType(slug=slugify(t), description=t) for t in type_list)


def _transform_grades(grade_list):
    """Returns a generator of a normalized Grade object"""
    return (models.Grade(slug=slugify(g), label=g) for g in grade_list)
