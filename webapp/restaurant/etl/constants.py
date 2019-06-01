import enum

BATCH_SIZE = 1000


class Headers(enum.Enum):
    """A collection of CSV headers"""
    RESTAURANT_CODES = "CAMIS"
    RESTAURANT_NAME = "DBA"
    BORO = "BORO"
    STREET = "STREET"
    ZIP_CODE = "ZIPCODE"
    PHONE = "PHONE"
    RESTAURANT_TYPES = "CUISINE DESCRIPTION"
    GRADES = "GRADE"
