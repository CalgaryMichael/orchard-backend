from enum import Enum, auto


class ChoiceEnum(Enum):
    """An enum that easily translates to a Django Choice field"""
    @classmethod
    def choices(cls):
        return list((choice.value, choice.name) for choice in cls)

    def __repr__(self):
        return str(self.value)

    def __str__(self):
        return str(self.value)


class CriticalRating(ChoiceEnum):
    NOT_APPLICABLE = 0
    NOT_CRITICAL = 1
    CRITICAL = 2

    @classmethod
    def from_slug(cls, slug):
        if slug is None:
            return
        slug_mapping = {
            "not-applicable": cls.NOT_APPLICABLE,
            "not-critical": cls.NOT_CRITICAL,
            "critical": cls.CRITICAL}
        return slug_mapping[slug]


class Boro(ChoiceEnum):
    BRONX = "bronx"
    BROOKLYN = "brooklyn"
    MANHATTAN = "manhattan"
    STATEN_ISLAND = "staten-island"
    QUEENS = "queens"
