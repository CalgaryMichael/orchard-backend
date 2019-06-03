import functools
import datetime
import pandas as pd
from webapp.restaurant import choices, models
from django.utils.text import slugify
from . import Headers


def normalize(value):
    """Normalizes Pandas NaN to python None"""
    return value if pd.isnull(value) is False else None


def transform_restaurant_types(type_list):
    """Returns a generator of normalized RestaurantType objects"""
    return (models.RestaurantType(slug=slugify(t), description=t) for t in type_list)


def _process_restaurants(restaurants, type_mapping):
    for restaurant in restaurants:
        restaurant_type = slugify(restaurant[Headers.RESTAURANT_TYPES.value])
        yield {
            "code": restaurant[Headers.RESTAURANT_CODES.value],
            "name": restaurant[Headers.RESTAURANT_NAME.value],
            "restaurant_type_id": type_mapping[restaurant_type]}


def transform_restaurants(restaurants):
    """Returns a generator of normalized Restaurant objects"""
    type_mapping = dict(models.RestaurantType.objects.all().values_list("slug", "id"))
    return (models.Restaurant(**restaurant) for restaurant in _process_restaurants(restaurants, type_mapping))


def _process_contacts(contacts, restaurant_mapping):
    for contact in contacts:
        restaurant = str(contact[Headers.RESTAURANT_CODES.value])
        yield {
            "restaurant_id": restaurant_mapping[restaurant],
            "boro": contact[Headers.BORO.value],
            "building_number": contact[Headers.BUILDING.value],
            "street": contact[Headers.STREET.value],
            "zip_code": contact[Headers.ZIP_CODE.value],
            "phone": contact[Headers.PHONE.value]}


def transform_restaurant_contacts(contacts):
    """Returns a generator of normalized Restaurant objects"""
    restaurant_mapping = dict(models.Restaurant.objects.all().values_list("code", "id"))
    return (models.RestaurantContact(**contact) for contact in _process_contacts(contacts, restaurant_mapping))


def transform_grades(grade_list):
    """Returns a generator of normalized Grade objects"""
    return (models.Grade(slug=slugify(g), label=g) for g in grade_list)


def transform_inspection_types(inspection_types):
    """Returns a generator of normalized InspectionType objects"""
    return (models.InspectionType(slug=slugify(i), description=i) for i in inspection_types)


def _convert_date(date_string):
    """Convert a string into a Date object or None"""
    if pd.isnull(date_string):
        return
    try:
        converted = datetime.datetime.strptime(date_string, "%m/%d/%y")
    except Exception:
        converted = datetime.datetime.strptime(date_string, "%m/%d/%Y")
    return converted.date()


def _process_inspections(inspections, restaurant_mapping, grade_mapping, type_mapping):
    for inspection in inspections:
        restaurant = str(inspection[Headers.RESTAURANT_CODES.value])
        grade = normalize(inspection[Headers.GRADES.value])
        inspection_type = normalize(inspection[Headers.INSPECTION_TYPE.value])
        grade_date = inspection[Headers.GRADE_DATE.value]
        inspection_date = inspection[Headers.INSPECTION_DATE.value]
        yield {
            "restaurant_id": restaurant_mapping[restaurant],
            "grade_id": grade_mapping[slugify(grade)] if grade is not None else None,
            "grade_date": _convert_date(grade_date),
            "inspection_type_id": type_mapping[slugify(inspection_type)] if inspection_type is not None else None,
            "inspection_date": _convert_date(inspection_date),
            "score": normalize(inspection[Headers.INSPECTION_SCORE.value])}


def transform_inspections(inspections):
    """Returns a generator of normalized Inspection objects"""
    restaurant_mapping = dict(models.Restaurant.objects.all().values_list("code", "id"))
    grade_mapping = dict(models.Grade.objects.all().values_list("slug", "id"))
    type_mapping = dict(models.InspectionType.objects.all().values_list("slug", "id"))
    inspection_generator = _process_inspections(inspections, restaurant_mapping, grade_mapping, type_mapping)
    return (models.Inspection(**inspection) for inspection in inspection_generator)


def _get_inspection_id(violation):
    """Finds the associated Inspection ID for a row of extracted Violation data"""
    inspection_date = _convert_date(violation[Headers.INSPECTION_DATE.value])
    restaurant_code = str(violation[Headers.RESTAURANT_CODES.value])
    inspection = (models.Inspection.objects
                  .filter(inspection_date=inspection_date, restaurant__code=restaurant_code)
                  .only("id"))
    return inspection.get().id


def _process_violations(violations):
    for violation in violations:
        inspection_id = _get_inspection_id(violation)
        critical_rating = choices.CriticalRating.from_slug(slugify(violation[Headers.CRITICAL_RATING.value]))
        yield {
            "inspection_id": inspection_id,
            "code": violation[Headers.VIOLATION_CODE.value],
            "critical_rating": critical_rating.value,
            "description": normalize(violation[Headers.VIOLATION_DESCRIPTION.value])}


def transform_violations(violations):
    """Returns a generator of normalized Inspection objects"""
    return (models.Violation(**violation) for violation in _process_violations(violations))
