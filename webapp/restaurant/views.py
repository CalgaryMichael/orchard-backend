from rest_framework import viewsets, pagination
from . import models, serializers


class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 1000


class RestaurantViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Restaurant.objects.all()
    serializer_class = serializers.RestaurantSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = models.Restaurant.objects.all()
        restaurant_type = self.request.query_params.get("restaurant_type", None)
        if restaurant_type is not None:
            queryset = queryset.filter(restaurant_type__slug=restaurant_type)
        minimum_grade = self.request.query_params.get("minimum_grade", None)
        if minimum_grade is not None:
            queryset = queryset.minimum_grade(minimum_grade)
        return (queryset
                .select_related("restaurantcontact", "restaurant_type")
                .prefetch_related("inspection_set")
                .order_by('id', 'code'))
