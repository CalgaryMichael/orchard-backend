from webapp.restaurant import models
from django.utils.text import slugify


def _transform_restaurant_types(type_list):
    """Returns a generator of a normalized RestaurantType object"""
    return (models.RestaurantType(slug=slugify(t), description=t) for t in type_list)
