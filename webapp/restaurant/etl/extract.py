import pandas as pd
import numpy as np
from django.utils.text import slugify
from . import Headers


def _extract_restaurant_types(csv):
    """Normalize data for RestaurantType model transformation"""
    restaurant_types = csv[Headers.RESTAURANT_TYPES].apply(lambda x: x.title())
    return (restaurant_type for restaurant_type in restaurant_types.unique())


def _extract_restaurants(csv):
    """Normalize data for Restaurant model transformation"""
    columns = [Headers.RESTAURANT_CODES, Headers.RESTAURANT_NAME, Headers.RESTAURANT_TYPES]
    restaurants = csv[columns].drop_duplicates(subset=Headers.RESTAURANT_CODES, keep="first")
    return restaurants.to_dict(orient="records")


def _extract_restaurant_contacts(csv):
    """Normalize data for RestaurantContact model transformation"""
    columns = [
        Headers.RESTAURANT_CODES,
        Headers.BORO,
        Headers.BUILDING,
        Headers.STREET,
        Headers.ZIP_CODE,
        Headers.PHONE]
    restaurants = csv[columns].drop_duplicates(subset=Headers.RESTAURANT_CODES, keep="first")
    return restaurants.to_dict(orient="records")


def _extract_grades(csv):
    """Normalize data for Grade model transformation"""
    grades = csv[Headers.GRADES].replace("", np.nan).dropna()
    return (grade for grade in grades.unique())


def _extract_inspections(csv):
    """Normalize data for Inspection model transformation"""
    columns = [
        Headers.RESTAURANT_CODES,
        Headers.INSPECTION_TYPE,
        Headers.INSPECTION_DATE,
        Headers.INSPECTION_SCORE,
        Headers.GRADES,
        Headers.GRADE_DATE]
    return csv[columns].to_dict(orient="record")
