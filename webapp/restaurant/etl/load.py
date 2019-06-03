import itertools
from django.conf import settings
from django.db import transaction
from webapp.restaurant import models
from . import constants


def chunk(gen):
    with transaction.atomic():
        while True:
            batch = list(itertools.islice(gen, settings.BATCH_SIZE))
            if not batch:
                break
            yield batch


@transaction.atomic
def load_restaurant_types(restaurant_types):
    """Load RestaurantType objects into database"""
    return models.RestaurantType.objects.bulk_create(restaurant_types)


def load_restaurants(restaurants):
    """Load Restaurant objects into database"""
    for batch in chunk(restaurants):
        models.Restaurant.objects.bulk_create(batch, settings.BATCH_SIZE)


def load_restaurant_contacts(contacts):
    """Load RestaurantContact objects into database"""
    for batch in chunk(contacts):
        models.RestaurantContact.objects.bulk_create(batch, settings.BATCH_SIZE)


def load_grades(grades):
    """Load Grade objects into database"""
    return models.Grade.objects.bulk_create(grades)


def load_inspection_types(inspection_types):
    """Load InspectionType objects into database"""
    for batch in chunk(inspection_types):
        models.InspectionType.objects.bulk_create(batch, settings.BATCH_SIZE)


def load_inspections(inspections):
    """Load Inspection objects into database"""
    for batch in chunk(inspections):
        models.Inspection.objects.bulk_create(batch, settings.BATCH_SIZE)


def load_violations(violations):
    """Load Violation objects into database"""
    for batch in chunk(violations):
        models.Violation.objects.bulk_create(batch, settings.BATCH_SIZE)
