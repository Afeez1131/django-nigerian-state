from django.test import TestCase

from nigerian_states.models import GeoPoliticalZone, State
from nigerian_states.utils import queryset_to_list
from .defaults import get_state, load_fixtures, get_random_state_in_zone
from nigerian_states.templatetags.state_tags import (
    default_zone,
    get_capital,
    get_lgas_in_state,
    get_states_in_zone,
    get_zone,
    get_zone_info,
    is_lga_in_state,
    is_state_in_zone,
)
from django.conf import settings


class TestTemplateTags(TestCase):
    """
    Test cases for the template tags
    """

    def setUp(self):
        load_fixtures()

        # def test_tags_get_states(self):
        """
        I don't think you need to render a template in order to test your filter logic. Django already has well-tested template rendering logic, which the unit-tests for your filter shouldn't have to worry about since the "job" done by your filter is not to render to a template, but to take an input and return an output.

        https://stackoverflow.com/questions/49603388/test-a-custom-template-tag-filter-in-django
        I agree with the above, which is why i won't be testing the tags using Template.
        # Test that `get_states` template tags returns states from the zone name passed as args.
        # """
        # zone_name = "North Central"
        # state = get_random_state_in_zone(zone_name)
        # context = Context({'zone_name': zone_name})
        # self.GET_STATES = Template(
        #     "{% load default_tags %}{% get_states_in_zone zone_name as states %}{{ states|safe }}"
        # )
        # rendered = self.GET_STATES.render(context)
        # self.assertIn(state.name, rendered)

    def test_tag_get_state_in_zone(self):
        """
        Test that template tag `get_states_in_zones` return states in a GeoPoliticalzone if a valid zone name is provided as args else empty list.
        """
        zone_name = "North Central"
        zone = GeoPoliticalZone.objects.get(name=zone_name)
        state = get_random_state_in_zone(zone_name)
        states_in_zones = get_states_in_zone(zone_name)
        self.assertIsInstance(states_in_zones, list)
        self.assertIn(state.name, states_in_zones)
        self.assertEqual(zone.total_states, len(states_in_zones))
        self.assertEqual(get_states_in_zone("Invalid Zone"), [])
        self.assertEqual(len(get_states_in_zone("Invalid Zone")), 0)

    def test_tag_get_capital(self):
        """
        Test that the `get_capital` returns the capital of the state provided if valid name of state was provided else ""
        """
        state = State.objects.get(name="Lagos")
        self.assertIsInstance(get_capital(state.name), str)
        self.assertEqual(get_capital(state.name), "Ikeja")
        self.assertEqual(get_capital("Oyo"), "Ibadan")
        self.assertEqual(get_capital("Kwara"), "Ilorin")
        self.assertEqual(get_capital("Togo"), "")

    def test_tag_get_lgas_in_state(self):
        """
        Test that the tag `get_lgas_in_state` returns all lgas in a state if a valid name of state is provided else returns "".
        """
        oyo_state = get_state("Oyo")
        all_lgas_oyo = get_lgas_in_state(oyo_state.name)
        self.assertIn("Ogbomosho North", get_lgas_in_state(oyo_state.name))
        self.assertEqual(len(all_lgas_oyo), oyo_state.total_lgas)

        lagos = get_state("Lagos")
        all_lgas_lagos = get_lgas_in_state(lagos.name)
        self.assertIsInstance(get_lgas_in_state(lagos.name), list)
        self.assertIn("Badagry", get_lgas_in_state(lagos.name))
        self.assertEqual(len(all_lgas_lagos), lagos.total_lgas)
        self.assertEqual(get_lgas_in_state("Togo"), [])
        self.assertEqual(get_lgas_in_state("Dubai"), [])

    def test_tag_is_state_in_zone(self):
        """
        Test that tag returns True if a state is in a zone or False if not.
        """
        self.assertIsInstance(is_state_in_zone("South West", "Oyo"), bool)
        self.assertTrue(is_state_in_zone("South West", "Oyo"))
        self.assertTrue(is_state_in_zone("South West", "Lagos"))
        self.assertTrue(is_state_in_zone("North West", "Kano"))
        self.assertFalse(is_state_in_zone("South South", "Oyo"))
        self.assertFalse(is_state_in_zone("South South", "Lagos"))

    def test_tag_is_lga_in_state(self):
        """
        Test that tag `is_lga_in_state` returns True if lga is in state else False
        """
        self.assertIsInstance(is_lga_in_state("Oyo", "Surulere"), bool)
        self.assertTrue(is_lga_in_state("Oyo", "Ogbomosho North"))
        self.assertTrue(is_lga_in_state("Abia", "Aba South"))
        self.assertTrue(is_lga_in_state("Kano", "Ungogo"))
        self.assertFalse(is_lga_in_state("Lagos", "Invalid LGA"))
        self.assertFalse(is_lga_in_state("Invalid State", "Invalid LGA"))

    def test_tag_get_zone(self):
        """
        Test that tag `get_zone` returns the name of the zone the state belongs to if a valid state, else ''
        """
        self.assertEqual(get_zone("Oyo"), "South West")
        self.assertEqual(get_zone("Lagos"), "South West")
        self.assertEqual(get_zone("Kano"), "North West")
        self.assertEqual(get_zone("Invalid State"), "")

    def test_tag_get_zone_info(self):
        """
        Test that the `get_zone_info` returns
        {
            "zone": zone name,
            "no of states": no of states,
            "states": [list of states]
            "no of lgas": no of lgas,
            "lgas": [list of lgas]
        }
        if valid zone name else {}
        """
        zone_name = "North Central"
        geo_zone = GeoPoliticalZone.objects.get(name=zone_name)
        data = {
            "zone": zone_name,
            "no_of_states": geo_zone.total_states,
            "states": queryset_to_list(geo_zone.all_states, "name"),
            "no_of_lgas": geo_zone.total_lgas,
            "lgas": queryset_to_list(geo_zone.all_lgas, "name"),
        }
        test_data = get_zone_info(zone_name)
        self.assertIsInstance(test_data, dict)
        self.assertEqual(test_data, data)
        self.assertIsInstance(test_data["states"], list)
        self.assertIsInstance(test_data["lgas"], list)

    def test_tag_default_zone(self):
        """
        Test that the `default zone` tag returns the default set in the settings
        """
        self.assertEqual(
            default_zone(), getattr(settings, "DEFAULT_GEO_POLITICAL_ZONES", [])
        )
