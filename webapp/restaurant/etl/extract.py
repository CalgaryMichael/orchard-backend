import pandas as pd
import numpy as np
from django.utils.text import slugify
from . import Headers


def extract_restaurant_types(csv):
    """Normalize data for RestaurantType model transformation"""
    restaurant_types = csv[Headers.RESTAURANT_TYPES.value].apply(lambda x: x.title())
    return (restaurant_type for restaurant_type in restaurant_types.unique())


def extract_restaurants(csv):
    """Normalize data for Restaurant model transformation"""
    columns = [
        Headers.RESTAURANT_CODES.value,
        Headers.RESTAURANT_NAME.value,
        Headers.RESTAURANT_TYPES.value]
    restaurants = csv[columns].drop_duplicates(subset=Headers.RESTAURANT_CODES.value, keep="first")
    return restaurants.to_dict(orient="records")


def extract_restaurant_contacts(csv):
    """Normalize data for RestaurantContact model transformation"""
    columns = [
        Headers.RESTAURANT_CODES.value,
        Headers.BORO.value,
        Headers.BUILDING.value,
        Headers.STREET.value,
        Headers.ZIP_CODE.value,
        Headers.PHONE.value]
    restaurants = csv[columns].drop_duplicates(subset=Headers.RESTAURANT_CODES.value, keep="first")
    return restaurants.to_dict(orient="records")


def extract_grades(csv):
    """Normalize data for Grade model transformation"""
    grades = csv[Headers.GRADES.value].replace("", np.nan).dropna()
    return (grade for grade in grades.unique())


def extract_inspection_types(csv):
    """Normalize data for InspectionType model transformation"""
    inspection_types = csv[Headers.INSPECTION_TYPE.value].dropna()
    return (inspection_type for inspection_type in inspection_types.unique())


def extract_inspections(csv):
    """Normalize data for Inspection model transformation"""
    columns = [
        Headers.RESTAURANT_CODES.value,
        Headers.INSPECTION_TYPE.value,
        Headers.INSPECTION_DATE.value,
        Headers.INSPECTION_SCORE.value,
        Headers.GRADES.value,
        Headers.GRADE_DATE.value]
    grades = csv[columns].drop_duplicates(subset=[Headers.RESTAURANT_CODES.value, Headers.INSPECTION_DATE.value])
    return grades.to_dict(orient="record")


def extract_violations(csv):
    """Normalize data for Violation model transformation"""
    columns = [
        Headers.RESTAURANT_CODES.value,
        Headers.INSPECTION_DATE.value,
        Headers.VIOLATION_CODE.value,
        Headers.VIOLATION_DESCRIPTION.value,
        Headers.CRITICAL_RATING.value]
    return csv[columns].to_dict(orient="records")
