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


def transform_restaurants(restaurants):
    """Returns a generator of normalized Restaurant objects"""
    restaurant_mapping = list()
    type_mapping = dict(models.RestaurantType.objects.all().values_list("slug", "id"))
    for restaurant in restaurants:
        restaurant_type = slugify(restaurant[Headers.RESTAURANT_TYPES.value])
        restaurant_mapping.append({
            "code": restaurant[Headers.RESTAURANT_CODES.value],
            "name": restaurant[Headers.RESTAURANT_NAME.value],
            "restaurant_type_id": type_mapping[restaurant_type]})
    return (models.Restaurant(**restaurant) for restaurant in restaurant_mapping)


def transform_restaurant_contacts(contacts):
    """Returns a generator of normalized Restaurant objects"""
    contact_mapping = list()
    restaurant_mapping = dict(models.Restaurant.objects.all().values_list("code", "id"))
    for contact in contacts:
        restaurant = str(contact[Headers.RESTAURANT_CODES.value])
        contact_mapping.append({
            "restaurant_id": restaurant_mapping[restaurant],
            "boro": contact[Headers.BORO.value],
            "building_number": contact[Headers.BUILDING.value],
            "street": contact[Headers.STREET.value],
            "zip_code": contact[Headers.ZIP_CODE.value],
            "phone": contact[Headers.PHONE.value]})
    return (models.RestaurantContact(**contact) for contact in contact_mapping)


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
    return datetime.datetime.strptime(date_string, "%m/%d/%y").date()


def transform_inspections(inspections):
    """Returns a generator of normalized Inspection objects"""
    inspection_mapping = list()
    restaurant_mapping = dict(models.Restaurant.objects.all().values_list("code", "id"))
    grade_mapping = dict(models.Grade.objects.all().values_list("slug", "id"))
    type_mapping = dict(models.InspectionType.objects.all().values_list("slug", "id"))
    for inspection in inspections:
        restaurant = str(inspection[Headers.RESTAURANT_CODES.value])
        grade = normalize(inspection[Headers.GRADES.value])
        inspection_type = slugify(inspection[Headers.INSPECTION_TYPE.value])
        grade_date = inspection[Headers.GRADE_DATE.value]
        inspection_date = inspection[Headers.INSPECTION_DATE.value]
        inspection_mapping.append({
            "restaurant_id": restaurant_mapping[restaurant],
            "grade_id": grade_mapping[slugify(grade)] if grade is not None else None,
            "grade_date": _convert_date(grade_date),
            "inspection_type_id": type_mapping[inspection_type],
            "inspection_date": _convert_date(inspection_date),
            "score": normalize(inspection[Headers.INSPECTION_SCORE.value])})
    return (models.Inspection(**inspection) for inspection in inspection_mapping)


def _get_inspection_id(inspections, violation):
    """Finds the associated Inspection ID for a row of extracted Violation data"""
    inspection_date = datetime.datetime.strptime(violation[Headers.INSPECTION_DATE.value], "%m/%d/%y").date()
    inspection = inspections[
        (str(violation[Headers.RESTAURANT_CODES.value]) == inspections.restaurant__code)
        & (inspection_date == inspections.inspection_date)
    ]
    return inspection.id.values[0]


def transform_violations(violations):
    """Returns a generator of normalized Inspection objects"""
    violation_mapping = list()
    inspection_mapping = models.Inspection.objects.all().values("id", "inspection_date", "restaurant__code")
    inspections = pd.DataFrame.from_records(inspection_mapping)
    for violation in violations:
        inspection_id = _get_inspection_id(inspections, violation)
        critical_rating = choices.CriticalRating.from_slug(slugify(violation[Headers.CRITICAL_RATING.value]))
        violation_mapping.append({
            "inspection_id": inspection_id,
            "code": violation[Headers.VIOLATION_CODE.value],
            "critical_rating": critical_rating.value,
            "description": normalize(violation[Headers.VIOLATION_DESCRIPTION.value])
        })
    return (models.Violation(**violation) for violation in violation_mapping)
