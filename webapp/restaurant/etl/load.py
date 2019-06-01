import itertools
from webapp.restaurant import models
from . import constants


def chunk(gen):
    batch = list(itertools.islice(gen, constants.BATCH_SIZE))
    if batch:
        yield batch


def load_restaurant_types(restaurant_types):
    """Load RestaurantType objects into database"""
    return models.RestaurantType.objects.bulk_create(restaurant_types)


def load_restaurants(restaurants):
    loaded = list()
    for batch in chunk(restaurants):
        loaded += models.Restaurant.objects.bulk_create(batch, constants.BATCH_SIZE)
    return loaded


def load_grades(grades):
    """Load Grade objects into database"""
    return models.Grade.objects.bulk_create(grades)
