from rest_framework import filters, viewsets
from . import models, serializers


class RestaurantViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Restaurant.objects.all()
    serializer_class = serializers.RestaurantSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("=code", "restaurant_type__slug")

    def get_queryset(self):
        queryset = models.Restaurant.objects.all()
        minimum_grade = self.request.query_params.get("minimum_grade", None)
        if minimum_grade is not None:
            queryset = queryset.filter(inspection__grade__slug__lte=minimum_grade)
        return queryset
