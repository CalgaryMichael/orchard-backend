from webapp.restaurant import models
from django.utils.text import slugify


def create_restaurant_type(type_slug):
    """Helper function for creating a Restaurant and a RestaurantType"""
    return models.RestaurantType.objects.create(slug=type_slug, description=type_slug.title())


def create_restaurant(code, name, type_slug):
    """Helper function for creating a Restaurant and a RestaurantType"""
    restaurant_type, _ = models.RestaurantType.objects.get_or_create(slug=type_slug, description=type_slug.title())
    return models.Restaurant.objects.create(code=code, name=name, restaurant_type=restaurant_type)


def create_restaurant_contact(restaurant, boro, building_number=None, street=None, zip_code=None, phone=None):
    """Helper function for creating a RstaurantContact"""
    return models.RestaurantContact.objects.create(
        restaurant=restaurant,
        boro=boro,
        building_number=building_number,
        street=street,
        zip_code=zip_code,
        phone=phone)


def create_inspection_type(description):
    """Helper function for creating an InspectionType"""
    return models.InspectionType.objects.create(slug=slugify(description), description=description)


def create_inspection(restaurant, inspection_type, date, score, grade_slug=None):
    """Helper function for creating an Inspection with an InspectionType and Grade"""
    grade, grade_date = None, None
    if grade_slug is not None:
        grade, _ = models.Grade.objects.get_or_create(slug=grade_slug, label=grade_slug.title())
        grade_date = date
    inspetion_type_object, _ = models.InspectionType.objects.get_or_create(
        slug=slugify(inspection_type),
        description=inspection_type)
    return models.Inspection.objects.create(
        restaurant=restaurant,
        inspection_type=inspetion_type_object,
        inspection_date=date,
        score=score,
        grade=grade,
        grade_date=grade_date)


def create_grade(grade):
    """Helper funtion for creating a Grade"""
    return models.Grade.objects.create(slug=slugify(grade), label=grade)
