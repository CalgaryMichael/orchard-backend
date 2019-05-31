from rest_framework import serializers
from . import models


class InspectionSerializer(serializers.ModelSerializer):
    grade = serializers.StringRelatedField()

    class Meta:
        model = models.Inspection
        fields = ("inspection_date", "score", "grade", "grade_date", "inspection_type")


class RestaurantTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RestaurantType
        fields = ("id", "slug", "description")


class RestaurantContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RestaurantContact
        fields = ("boro", "building_number", "street", "zip_code", "phone")


class RestaurantSerializer(serializers.ModelSerializer):
    restaurant_type = serializers.StringRelatedField()
    contact = RestaurantContactSerializer(source="restaurantcontact")
    inspections = InspectionSerializer(many=True, source="inspection_set")

    class Meta:
        model = models.Restaurant
        fields = ("id", "code", "name", "restaurant_type", "contact", "inspections")
