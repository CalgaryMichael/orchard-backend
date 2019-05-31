from rest_framework import routers
from . import views


router = routers.SimpleRouter()
router.register(r"restaurants", views.RestaurantViewSet)
url_patterns = router.urls
