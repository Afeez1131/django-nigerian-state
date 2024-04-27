import random
from nigerian_states.models import GeoPoliticalZone, LocalGovernment, State
from django.core.management import call_command


EXPECTED_STATE_COUNT = 37
FIRST_STATE = "Abia"
FIRST_LG = "Aba North"
LAST_LG = "Municipal Area Council"
LAST_STATE = "Federal Capital Territory"
TOTAL_ZONES = 6
TOTAL_STATES = 37
TOTAL_LGAS = 774
FIRST_THREE_STATE = ["Abia", "Adamawa", "Akwa Ibom"]
LAST_THREE_STATE = ["Federal Capital Territory", "Zamfara", "Yobe"]
LAGOS_LGAS = 20
OYO_LGAS = 33


def get_random_zone():
    return random.choice(GeoPoliticalZone.objects.all())


def get_random_state():
    return random.choice(State.objects.all())


def get_random_lga():
    return random.choice(LocalGovernment.objects.all())


def load_fixtures():
    """
    Helper function to load fixtures data in the needed test function
    """
    return call_command(
        "loaddata", "nigerian_states/fixtures/fixtures.json", verbosity=0
    )


def get_random_state_in_zone(zone_name):
    zone = GeoPoliticalZone.objects.get(name=zone_name)
    return random.choice(zone.all_states)


def get_state(name):
    return State.objects.get(name=name)
