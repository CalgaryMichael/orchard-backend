from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from . import models


@admin.register(models.RestaurantType)
class RestaurantTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "slug", "description")


class RestaurantContactInline(admin.StackedInline):
    model = models.RestaurantContact


@admin.register(models.Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "style")
    inlines = (RestaurantContactInline,)

    def style(self, obj):
        if obj.restaurant_type:
            return obj.restaurant_type.description


@admin.register(models.Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ("id", "slug", "label")


class ViolationInline(admin.StackedInline):
    model = models.Violation


@admin.register(models.Inspection)
class InspectionAdmin(admin.ModelAdmin):
    list_display = ("id", "restaurant_link", "inspection_type", "inspection_date", "grade")
    list_filter = ("grade",)
    inlines = (ViolationInline,)

    def restaurant_link(self, obj):
        url = reverse("admin:restaurant_restaurant_changelist") + "?id__exact={}".format(obj.restaurant.id)
        return mark_safe("<a href='{0}'>{1}</a>".format(url, obj.restaurant))

    restaurant_link.short_description = "Restaurant"
