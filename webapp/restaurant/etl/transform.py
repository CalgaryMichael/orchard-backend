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
