import itertools
from django.conf import settings
from webapp.restaurant import models
from . import constants


def chunk(gen):
    while True:
        batch = list(itertools.islice(gen, settings.BATCH_SIZE))
        if not batch:
            break
        yield batch


def load_restaurant_types(restaurant_types):
    """Load RestaurantType objects into database"""
    return models.RestaurantType.objects.bulk_create(restaurant_types)


def load_restaurants(restaurants):
    """Load Restaurant objects into database"""
    loaded = list()
    for batch in chunk(restaurants):
        loaded += models.Restaurant.objects.bulk_create(batch, settings.BATCH_SIZE)
    return loaded


def load_restaurant_contacts(contacts):
    """Load RestaurantContact objects into database"""
    loaded = list()
    for batch in chunk(contacts):
        loaded += models.RestaurantContact.objects.bulk_create(batch, settings.BATCH_SIZE)
    return loaded


def load_grades(grades):
    """Load Grade objects into database"""
    return models.Grade.objects.bulk_create(grades)


def load_inspection_types(inspection_types):
    """Load InspectionType objects into database"""
    loaded = list()
    for batch in chunk(inspection_types):
        loaded += models.InspectionType.objects.bulk_create(batch, settings.BATCH_SIZE)
    return loaded


def load_inspections(inspections):
    """Load Inspection objects into database"""
    loaded = list()
    for batch in chunk(inspections):
        loaded += models.Inspection.objects.bulk_create(batch, settings.BATCH_SIZE)
    return loaded


def load_violations(violations):
    """Load Violation objects into database"""
    loaded = list()
    for batch in chunk(violations):
        loaded += models.Violation.objects.bulk_create(batch, settings.BATCH_SIZE)
    return loaded
