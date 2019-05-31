from django.db import models
from . import choices


class RestaurantType(models.Model):
    slug = models.SlugField(db_index=True)
    description = models.CharField(max_length=50)

    def __repr__(self):
        return "<RestaurantType {}>".format(self.slug)

    def __str__(self):
        return self.description


class Restaurant(models.Model):
    restaurant_type = models.ForeignKey(RestaurantType, on_delete=models.CASCADE)
    code = models.CharField(max_length=8, unique=True)
    name = models.CharField(max_length=200)

    def __repr__(self):
        return "<Restaurant {}>".format(self.code)

    def __str__(self):
        return "{0} ({1})".format(self.name, self.code)


class RestaurantContact(models.Model):
    restaurant = models.OneToOneField(Restaurant, on_delete=models.CASCADE)
    boro = models.CharField(choices=choices.Boro.choices(), null=True, max_length=25)
    building_number = models.PositiveSmallIntegerField(null=True)
    street = models.CharField(max_length=100, null=True)
    zip_code = models.CharField(max_length=7, null=True)
    phone = models.CharField(max_length=10, null=True)

    def __repr__(self):
        return "<RestaurantContact {} ({})>".format(self.boro, self.building_number)

    def __str__(self):
        return u"{0} ({1})".format(self.boro, self.building_number)


class Grade(models.Model):
    slug = models.SlugField(db_index=True)
    label = models.CharField(max_length=50)

    def __repr__(self):
        return "<Grade {}>".format(self.label)

    def __str__(self):
        return self.label


class Inspection(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    inspection_type = models.CharField(max_length=100)
    inspection_date = models.DateField(null=True)
    score = models.PositiveSmallIntegerField(null=True)
    grade = models.ForeignKey(Grade, null=True, on_delete=models.CASCADE)
    grade_date = models.DateField(null=True)

    def __repr__(self):
        return "<Inspection {}>".format(self.id)

    def __str__(self):
        return "{0} - {1}".format(self.restaurant.name, self.inspection_date)


class Violation(models.Model):
    inspection = models.OneToOneField(Inspection, on_delete=models.CASCADE)
    code = models.CharField(max_length=5)
    critical_rating = models.PositiveSmallIntegerField(choices=choices.CriticalRating.choices())
    description = models.CharField(max_length=100)

    def __repr__(self):
        return "<Violation {}>".format(self.code)

    def __str__(self):
        return "{0} - {1}".format(self.code, self.critical_rating)
