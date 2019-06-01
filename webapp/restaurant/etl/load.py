from webapp.restaurant import models


def load_restaurant_types(restaurant_types):
    """Load RestaurantType objects into database"""
    return models.RestaurantType.objects.bulk_create(restaurant_types)
