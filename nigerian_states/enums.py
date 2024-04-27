from django.db.models import TextChoices


class PoliticalZones(TextChoices):
    NORTH_CENTRAL = "North Central"
    NORTH_EAST = "North East"
    NORTH_WEST = "North West"
    SOUTH_EAST = "South East"
    SOUTH_SOUTH = "South South"
    SOUTH_WEST = "South West"
