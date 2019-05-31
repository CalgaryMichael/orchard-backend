import datetime
import pytest
import pytz
from webapp.restaurant import choices, models, serializers
from . import utils


@pytest.mark.django_db
def test_inspection_serializer__with_grade():
    """Test that the InspectionSerializer contains correct data with a Grade"""
    date = datetime.date(2018, 1, 1)
    restaurant = utils.create_restaurant(code="30004700", name="WENDY'S", type_slug="hamburgers")
    inspection = utils.create_inspection(
        restaurant=restaurant,
        inspection_type="Cycle Inspection / Initial Inspection",
        date=date,
        score=14,
        grade_slug="a")
    serializer = serializers.InspectionSerializer(inspection)
    expected_data = {
        "inspection_type": "Cycle Inspection / Initial Inspection",
        "inspection_date": "2018-01-01",
        "score": 14,
        "grade": "A",
        "grade_date": "2018-01-01"}
    assert serializer.data == expected_data


@pytest.mark.django_db
def test_inspection_serializer__without_grade():
    """Test that the InspectionSerializer contains correct data without a Grade"""
    date = datetime.date(2018, 1, 1)
    restaurant = utils.create_restaurant(code="30004700", name="WENDY'S", type_slug="hamburgers")
    inspection = utils.create_inspection(
        restaurant=restaurant,
        inspection_type="Cycle Inspection / Initial Inspection",
        date=date,
        score=14)
    serializer = serializers.InspectionSerializer(inspection)
    expected_data = {
        "inspection_type": "Cycle Inspection / Initial Inspection",
        "inspection_date": "2018-01-01",
        "score": 14,
        "grade": None,
        "grade_date": None}
    assert serializer.data == expected_data


@pytest.mark.django_db
def test_restaurant_type_serializer():
    restaurant_type = models.RestaurantType.objects.create(slug="hamburgers", description="Hamburgers")
    serializer = serializers.RestaurantTypeSerializer(restaurant_type)
    expected_data = {
        "id": 1,
        "slug": "hamburgers",
        "description": "Hamburgers"}
    assert serializer.data == expected_data


@pytest.mark.django_db
def test_restaurant_contact_serializer():
    restaurant = utils.create_restaurant(code="30004700", name="WENDY'S", type_slug="hamburgers")
    restaurant_contact = utils.create_restaurant_contact(
        restaurant=restaurant,
        boro=choices.Boro.BROOKLYN,
        building_number="100",
        street="123 Somewhere Ave.",
        zip_code="12345",
        phone="4445554444")
    serializer = serializers.RestaurantContactSerializer(restaurant_contact)
    expected_data = {
        "boro": "brooklyn",
        "building_number": 100,
        "street": "123 Somewhere Ave.",
        "zip_code": "12345",
        "phone": "4445554444"}
    assert serializer.data == expected_data


@pytest.mark.django_db
def test_restaurant_serializer__no_inspections():
    restaurant = utils.create_restaurant(code="30004700", name="WENDY'S", type_slug="hamburgers")
    utils.create_restaurant_contact(
        restaurant=restaurant,
        boro=choices.Boro.BROOKLYN,
        building_number="100",
        street="123 Somewhere Ave.",
        zip_code="12345",
        phone="4445554444")
    serializer = serializers.RestaurantSerializer(restaurant)
    expected_data = {
        "id": 1,
        "code": "30004700",
        "name": "WENDY'S",
        "restaurant_type": "Hamburgers",
        "contact": {
            "boro": "brooklyn",
            "building_number": 100,
            "street": "123 Somewhere Ave.",
            "zip_code": "12345",
            "phone": "4445554444"
        },
        "inspections": []}
    assert serializer.data == expected_data


@pytest.mark.django_db
def test_restaurant_serializer__one_inspection():
    date = datetime.date(2018, 1, 1)
    restaurant = utils.create_restaurant(code="30004700", name="WENDY'S", type_slug="hamburgers")
    utils.create_restaurant_contact(
        restaurant=restaurant,
        boro=choices.Boro.BROOKLYN,
        building_number="100",
        street="123 Somewhere Ave.",
        zip_code="12345",
        phone="4445554444")
    utils.create_inspection(
        restaurant=restaurant,
        inspection_type="Cycle Inspection / Initial Inspection",
        date=date,
        score=14)
    serializer = serializers.RestaurantSerializer(restaurant)
    expected_data = {
        "id": 1,
        "code": "30004700",
        "name": "WENDY'S",
        "restaurant_type": "Hamburgers",
        "contact": {
            "boro": "brooklyn",
            "building_number": 100,
            "street": "123 Somewhere Ave.",
            "zip_code": "12345",
            "phone": "4445554444"
        },
        "inspections": [
            {
                "inspection_type": "Cycle Inspection / Initial Inspection",
                "inspection_date": "2018-01-01",
                "score": 14,
                "grade": None,
                "grade_date": None
            }
        ]
    }
    assert serializer.data == expected_data


@pytest.mark.django_db
def test_restaurant_serializer__multiple_inspections():
    date = datetime.date(2018, 1, 1)
    restaurant = utils.create_restaurant(code="30004700", name="WENDY'S", type_slug="hamburgers")
    utils.create_restaurant_contact(
        restaurant=restaurant,
        boro=choices.Boro.BROOKLYN,
        building_number="100",
        street="123 Somewhere Ave.",
        zip_code="12345",
        phone="4445554444")
    utils.create_inspection(
        restaurant=restaurant,
        inspection_type="Cycle Inspection / Initial Inspection",
        date=date,
        score=14)
    utils.create_inspection(
        restaurant=restaurant,
        inspection_type="Cycle Inspection / Re-inspection",
        date=date + datetime.timedelta(days=30),
        grade_slug="a",
        score=10)
    serializer = serializers.RestaurantSerializer(restaurant)
    expected_data = {
        "id": 1,
        "code": "30004700",
        "name": "WENDY'S",
        "restaurant_type": "Hamburgers",
        "contact": {
            "boro": "brooklyn",
            "building_number": 100,
            "street": "123 Somewhere Ave.",
            "zip_code": "12345",
            "phone": "4445554444"
        },
        "inspections": [
            {
                "inspection_type": "Cycle Inspection / Initial Inspection",
                "inspection_date": "2018-01-01",
                "score": 14,
                "grade": None,
                "grade_date": None
            },
            {
                "inspection_type": "Cycle Inspection / Re-inspection",
                "inspection_date": "2018-01-31",
                "score": 10,
                "grade": "A",
                "grade_date": "2018-01-31"
            }
        ]
    }
    assert serializer.data == expected_data
