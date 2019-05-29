from django.db import models
from . import choices


class RestaurantType(models.Model):
    slug = models.SlugField(db_index=True)
    description = models.CharField(max_length=50)


class RestaurantContact(models.Model):
    boro = models.CharField(choices=choices.Boro.choices(), null=True, max_length=25)
    building_number = models.PositiveSmallIntegerField(null=True)
    street = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=7)
    phone = models.CharField(max_length=10)


class Restaurant(models.Model):
    restaurant_type = models.ForeignKey(RestaurantType, on_delete=models.CASCADE)
    contact = models.OneToOneField(RestaurantContact, on_delete=models.CASCADE)
    code = models.CharField(max_length=8)
    name = models.CharField(max_length=200)


class Grade(models.Model):
    slug = models.SlugField(db_index=True)
    label = models.CharField(max_length=50)


class Inspection(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    inspection_type = models.CharField(max_length=100)
    inspection_date = models.DateField(null=True)
    score = models.PositiveSmallIntegerField(null=True)
    grade = models.ForeignKey(Grade, null=True, on_delete=models.CASCADE)
    grade_date = models.DateField(null=True)


class Violation(models.Model):
    code = models.CharField(max_length=5)
    critical_rating = models.PositiveSmallIntegerField(choices=choices.CriticalRating.choices())
    description = models.CharField(max_length=100)
