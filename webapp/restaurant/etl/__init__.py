from .constants import Headers
from . import extract, load, transform


def etl(csv_buffer):
    """
    Handles the extraction, transformation, and loading of a CSV file.

    Due to the relationship of the database models, the transformation + loading
    needs to happen in the following order:
        - RestaurantType
        - Restaurant
        - RestaurantContact
        - Grade
        - InspectionType
        - Inspection
        - Violation
    """
    extracted = extract.extract_all(csv_buffer)
    _handle_restaurant_types(extracted)
    _handle_restaurants(extracted)
    _handle_restaurant_contacts(extracted)
    _handle_grades(extracted)
    _handle_inspection_types(extracted)
    _handle_inspections(extracted)
    _handle_violations(extracted)


def _handle_restaurant_types(extracted):
    """Transform and load the extracted RestaurantType models"""
    restaurant_types = transform.transform_restaurant_types(extracted["restaurant_types"])
    load.load_restaurant_types(restaurant_types)


def _handle_restaurants(extracted):
    """Transform and load the extracted Restaurant models"""
    restaurants = transform.transform_restaurants(extracted["restaurants"])
    load.load_restaurants(restaurants)


def _handle_restaurant_contacts(extracted):
    """Transform and load the extracted RestaurantContact models"""
    contacts = transform.transform_restaurant_contacts(extracted["restaurant_contacts"])
    load.load_restaurant_contacts(contacts)


def _handle_grades(extracted):
    """Transform and load the extracted Grade models"""
    grades = transform.transform_grades(extracted["grades"])
    load.load_grades(grades)


def _handle_inspection_types(extracted):
    """Transform and load the extracted InspectionType models"""
    inspection_types = transform.transform_inspection_types(extracted["inspection_types"])
    load.load_inspection_types(inspection_types)


def _handle_inspections(extracted):
    """Transform and load the extracted InspectionType models"""
    inspections = transform.transform_inspections(extracted["inspections"])
    load.load_inspections(inspections)


def _handle_violations(extracted):
    """Transform and load the extracted Violation models"""
    violations = transform.transform_violations(extracted["violations"])
    load.load_violations(violations)
