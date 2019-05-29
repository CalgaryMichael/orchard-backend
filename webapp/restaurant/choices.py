from enum import Enum, auto


class ChoiceEnum(Enum):
    """An enum that easily translates to a Django Choice field"""
    @classmethod
    def choices(cls):
        return list((choice.value, choice.name) for choice in cls)


class CriticalRating(ChoiceEnum):
    NOT_APPLICABLE = 0
    NOT_CRITICAL = 1
    CRITICAL = 2


class Boro(ChoiceEnum):
    BRONX = "bronx"
    BROOKLYN = "brooklyn"
    MANHATTAN = "manhattan"
    STATEN_ISLAND = "staten-island"
    QUEENS = "queens"
