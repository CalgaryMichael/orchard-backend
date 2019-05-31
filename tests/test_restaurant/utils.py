from webapp.restaurant import models


def create_restaurant(code, name, type_slug):
    """Helper function for creating a Restaurant and a RestaurantType"""
    restaurant_type, _ = models.RestaurantType.objects.get_or_create(slug=type_slug, description=type_slug.title())
    return models.Restaurant.objects.create(code=code, name=name, restaurant_type=restaurant_type)


def create_restaurant_contact(restaurant, boro, building_number=None, street=None, zip_code=None, phone=None):
    return models.RestaurantContact.objects.create(
        restaurant=restaurant,
        boro=boro,
        building_number=building_number,
        street=street,
        zip_code=zip_code,
        phone=phone)


def create_inspection(restaurant, inspection_type, date, score, grade_slug=None):
    """Helper function for creating an Inspection with a Grade"""
    grade, grade_date = None, None
    if grade_slug is not None:
        grade, _ = models.Grade.objects.get_or_create(slug=grade_slug, label=grade_slug.title())
        grade_date = date
    return models.Inspection.objects.create(
        restaurant=restaurant,
        inspection_type=inspection_type,
        inspection_date=date,
        score=score,
        grade=grade,
        grade_date=grade_date)
