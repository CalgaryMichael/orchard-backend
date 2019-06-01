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
    restaurants = csv.drop_duplicates(subset=Headers.RESTAURANT_CODES, keep="first")
    return restaurants.to_dict(orient="records")


def _extract_grades(csv):
    """Normalize data for Grade model transformation"""
    grades = csv[Headers.GRADES].replace("", np.nan).dropna()
    return (grade for grade in grades.unique())
