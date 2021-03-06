from django.db import models
from django.db.models.aggregates import Max
from . import choices


class RestaurantType(models.Model):
    slug = models.SlugField(max_length=100, db_index=True)
    description = models.CharField(max_length=100)

    def __repr__(self):
        return "<RestaurantType {}>".format(self.slug)

    def __str__(self):
        return self.description


class RestaurantQuerySet(models.QuerySet):
    def minimum_grade(self, minimum_grade):
        query = self.annotate(minimum_grade=Max("inspection__grade__slug"))
        return query.filter(minimum_grade__lte=minimum_grade)


class Restaurant(models.Model):
    restaurant_type = models.ForeignKey(RestaurantType, db_index=True, on_delete=models.CASCADE)
    code = models.CharField(max_length=8, db_index=True, unique=True)
    name = models.CharField(max_length=200)
    objects = RestaurantQuerySet.as_manager()

    def __repr__(self):
        return "<Restaurant {}>".format(self.code)

    def __str__(self):
        return "{0} ({1})".format(self.name, self.code)


class RestaurantContact(models.Model):
    restaurant = models.OneToOneField(Restaurant, on_delete=models.CASCADE)
    boro = models.CharField(choices=choices.Boro.choices(), null=True, max_length=25)
    building_number = models.CharField(max_length=15, null=True)
    street = models.CharField(max_length=100, null=True)
    zip_code = models.CharField(max_length=7, null=True)
    phone = models.CharField(max_length=12, null=True)

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


class InspectionType(models.Model):
    slug = models.SlugField(max_length=100)
    description = models.CharField(max_length=100)

    def __repr__(self):
        return "<InspectionType {}>".format(self.id)

    def __str__(self):
        return self.description


class Inspection(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    inspection_type = models.ForeignKey(InspectionType, null=True, on_delete=models.CASCADE)
    inspection_date = models.DateField(null=True)
    score = models.IntegerField(null=True)
    grade = models.ForeignKey(Grade, null=True, on_delete=models.CASCADE)
    grade_date = models.DateField(null=True)

    def __repr__(self):
        return "<Inspection {}>".format(self.id)

    def __str__(self):
        return "{0} - {1}".format(self.restaurant.name, self.inspection_date)


class Violation(models.Model):
    inspection = models.ForeignKey(Inspection, on_delete=models.CASCADE)
    code = models.CharField(max_length=5)
    critical_rating = models.PositiveSmallIntegerField(choices=choices.CriticalRating.choices())
    description = models.TextField(null=True)

    def __repr__(self):
        return "<Violation {}>".format(self.code)

    def __str__(self):
        return "{0} - {1}".format(self.code, self.critical_rating)
