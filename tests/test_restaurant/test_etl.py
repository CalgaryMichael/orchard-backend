import io
import os
import pytest
from webapp.restaurant import etl, models
from . import data_folder


@pytest.mark.django_db
def test_etl():
    with io.open(os.path.join(data_folder, "inspection_violations.csv"), "r", encoding="ISO-8859-1") as csv_buffer:
        etl.etl(csv_buffer)
    assert models.RestaurantType.objects.all().count() == 23
    assert models.Restaurant.objects.all().count() == 61
    assert models.RestaurantContact.objects.all().count() == 61
    assert models.Grade.objects.all().count() == 4
    assert models.InspectionType.objects.all().count() == 13
    assert models.Inspection.objects.all().count() == 340
    assert models.Violation.objects.all().count() == 999
