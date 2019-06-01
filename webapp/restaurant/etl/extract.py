import pandas as pd
import numpy as np
from django.utils.text import slugify
from . import load

RESTAURANT_TYPES = "CUISINE DESCRIPTION"


def _extract_restaurant_types(csv):
    """Normalize data for RestaurantType models"""
    restaurant_types = csv[RESTAURANT_TYPES].apply(lambda x: x.title())
    return (restaurant_type for restaurant_type in restaurant_types.unique())
