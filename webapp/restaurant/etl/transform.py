import functools
import datetime
from webapp.restaurant import models
from django.utils.text import slugify
from . import Headers


def _transform_restaurant_types(type_list):
    """Returns a generator of normalized RestaurantType objects"""
    return (models.RestaurantType(slug=slugify(t), description=t) for t in type_list)


def _transform_restaurants(restaurants):
    """Returns a generator of normalized Restaurant objects"""
    restaurant_mapping = list()
    type_mapping = dict(models.RestaurantType.objects.all().values_list("slug", "id"))
    for restaurant in restaurants:
        restaurant_type = slugify(restaurant[Headers.RESTAURANT_TYPES])
        restaurant_mapping.append({
            "code": restaurant[Headers.RESTAURANT_CODES],
            "name": restaurant[Headers.RESTAURANT_NAME],
            "restaurant_type_id": type_mapping[restaurant_type]})
    return (models.Restaurant(**restaurant) for restaurant in restaurant_mapping)


def _transform_restaurant_contacts(contacts):
    """Returns a generator of normalized Restaurant objects"""
    contact_mapping = list()
    restaurant_mapping = dict(models.Restaurant.objects.all().values_list("code", "id"))
    for contact in contacts:
        restaurant = contact[Headers.RESTAURANT_CODES]
        contact_mapping.append({
            "restaurant_id": restaurant_mapping[restaurant],
            "boro": contact[Headers.BORO],
            "building_number": contact[Headers.BUILDING],
            "street": contact[Headers.STREET],
            "zip_code": contact[Headers.ZIP_CODE],
            "phone": contact[Headers.PHONE]})
    return (models.RestaurantContact(**contact) for contact in contact_mapping)


def _transform_grades(grade_list):
    """Returns a generator of normalized Grade objects"""
    return (models.Grade(slug=slugify(g), label=g) for g in grade_list)


def _convert_date(date_string):
    """Convert a string into a Date object or None"""
    return datetime.datetime.strptime(date_string, "%m/%d/%Y").date() if date_string else None


def _transform_inspections(inspections):
    """Returns a generator of normalized Inspection objects"""
    inspection_mapping = list()
    restaurant_mapping = dict(models.Restaurant.objects.all().values_list("code", "id"))
    grade_mapping = dict(models.Grade.objects.all().values_list("slug", "id"))
    type_mapping = dict(models.InspectionType.objects.all().values_list("slug", "id"))
    for inspection in inspections:
        restaurant = inspection[Headers.RESTAURANT_CODES]
        grade = inspection[Headers.GRADES]
        inspection_type = slugify(inspection[Headers.INSPECTION_TYPE])
        grade_date = inspection[Headers.GRADE_DATE]
        inspection_date = inspection[Headers.INSPECTION_DATE]
        inspection_mapping.append({
            "restaurant_id": restaurant_mapping[restaurant],
            "grade_id": grade_mapping[slugify(grade)] if grade is not None else None,
            "grade_date": _convert_date(grade_date),
            "inspection_type_id": type_mapping[inspection_type],
            "inspection_date": _convert_date(inspection_date),
            "score": inspection[Headers.INSPECTION_SCORE]})
    return (models.Inspection(**inspection) for inspection in inspection_mapping)
