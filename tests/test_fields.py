from django.core.exceptions import ValidationError
from nigerian_states.enums import PoliticalZones
from nigerian_states.models import GeoPoliticalZone, State, LocalGovernment
from django.test import TestCase, override_settings
from django.conf import settings

from nigerian_states.utils import queryset_to_list
from .defaults import (
    FIRST_LG,
    FIRST_STATE,
    FIRST_THREE_STATE,
    LAST_LG,
    LAST_STATE,
    LAST_THREE_STATE,
    load_fixtures,
    TOTAL_ZONES,
    TOTAL_STATES,
    TOTAL_LGAS,
)
from django import forms

from nigerian_states.fields import (
    BaseField,
    GeoPoliticalZoneField,
    StateField,
    LocalGovernmentField,
)


DEFAULT_POLITICAL_ZONES = getattr(settings, "DEFAULT_GEO_POLITICAL_ZONES", [])


@override_settings(DEFAULT_GEO_POLITICAL_ZONES=[])
class BaseFieldTestCase(TestCase):
    def test_base_field_before_loading_data(self):
        """
        Test for the BaseField which the custom forms inherit form.
        """
        field = BaseField()
        self.assertListEqual(field.zones, [])
        self.assertEqual(field.empty_label, None)
        self.assertEqual(len(field.get_zones()), 6)
        self.assertIsInstance(field.get_zones(), list)
        self.assertListEqual(field.choices, [("", "")])


class GeoPoliticalFieldTestCase(TestCase):
    """
    Test Case for GeoPoliticalZone.
    """

    def test_geo_political_zone_initialization_without_data(self):
        """
        Test the initialization of GeoPoliticalZoneField without data in db.
        """
        with override_settings(DEFAULT_GEO_POLITICAL_ZONES=[]):
            field = GeoPoliticalZoneField()
            self.assertIsInstance(field, GeoPoliticalZoneField)
            self.assertEqual(field.empty_label, None)
            self.assertEqual(field.zones, [])
            self.assertEqual(field.choices, [("", "Select a Geo-Political Zone")])
            with self.assertRaises(ValidationError):
                field.clean("Sokoto")
            self.assertEqual(len(field.get_choices()), 1)
            self.assertEqual(len(field.get_zones()), TOTAL_ZONES)

    def test_geo_political_zone_initialization_with_data(self):
        """
        Test the initialization of GeoPoliticalZoneField with data in DB.
        """
        load_fixtures()
        with override_settings(
            DEFAULT_GEO_POLITICAL_ZONES=["North West", "South South"]
        ):
            field = GeoPoliticalZoneField()
            default_zone = sorted(getattr(settings, "DEFAULT_GEO_POLITICAL_ZONES", []))
            default_zone = GeoPoliticalZone.objects.filter(name__in=default_zone)
            default_choices = [("", "Select a Geo-Political Zone")]
            default_choices += [(zn.name, zn.name) for zn in default_zone]
            # print(getattr(settings, 'DEFAULT_GEO_POLITICAL_ZONES', []))
            self.assertIsInstance(field, GeoPoliticalZoneField)
            self.assertEqual(field.empty_label, None)
            self.assertEqual(field.zones, [])
            self.assertEqual(field.choices[0], ("", "Select a Geo-Political Zone"))
            self.assertEqual(len(field.get_zones()), 2)
            self.assertEqual(len(field.get_choices()), 3)
            self.assertListEqual(field.get_choices(), default_choices)
            self.assertEqual(
                sorted(field.get_zones()),
                sorted(queryset_to_list(default_zone, "name")),
            )
            a_choice = default_choices[1][0]
            self.assertEqual(field.clean(a_choice), a_choice)
            with self.assertRaises(ValidationError):
                self.assertEqual(field.clean("North Central"), "North Central")

    def test_geo_political_zone_field_without_default_zone(self):
        """
        Test the GeoPoliticalZoneField initialization without default zones, or kwargs zones, or data in DB
        """
        field = GeoPoliticalZoneField()
        self.assertEqual(len(field.choices), 1)  # the empty label
        self.assertListEqual(field.choices, [("", "Select a Geo-Political Zone")])
        with self.assertRaises(ValidationError):
            field.clean("North Central")

    def test_geo_political_zone_initialization_with_data_and_kwargs(self):
        """
        Test GeoPoliticalZoneField initialization with kwargs (label, empty_label, zones, widget etc.) with data in DB
        """
        load_fixtures()
        zones = ["North Central", "North West", "South East"]
        field = GeoPoliticalZoneField(
            label="GeoPolitical Zone",
            empty_label="Select a Zone",
            zones=zones,
            help_text="Select a GeoPolitical Zone",
            widget=forms.Select(attrs={"class": "form-select"}),
        )
        self.assertEqual(field.label, "GeoPolitical Zone")
        self.assertEqual(field.empty_label, "Select a Zone")
        self.assertListEqual(field.zones, zones)
        self.assertEqual(field.help_text, "Select a GeoPolitical Zone")
        self.assertTupleEqual(field.choices[0], ("", "Select a Zone"))
        with self.assertRaises(ValidationError):
            field.clean("North North")
        self.assertNotIn(("North North"), field.choices)
        self.assertListEqual(sorted(field.zones), sorted(field.get_zones()))
        self.assertEqual(field.clean("South East"), "South East")
        self.assertEqual(len(field.choices), len(zones) + 1)

    @override_settings(DEFAULT_GEO_POLITICAL_ZONES=["North West", "South South"])
    def test_geo_political_zone_default_overriding(self):
        """
        Test that the GeoPoliticalZoneField, zones kwargs override the settings.DEFAULT_GEO_POLITICAL_ZONES
        """
        load_fixtures()
        field = GeoPoliticalZoneField(zones=["South West", "South East"])
        default = getattr(settings, "DEFAULT_GEO_POLITICAL_ZONES", [])
        self.assertNotEqual(default, field.zones)
        self.assertEqual(
            sorted(["South West", "South East"]),
            sorted([item[0] for item in field.choices[1:]]),
        )

    def test_geo_political_zone_widget(self):
        """
        Test the GeoPoliticalZoneField widget attrs.
        """
        field = GeoPoliticalZoneField(
            widget=forms.Select(attrs={"class": "form-select"})
        )
        widget = field.widget
        self.assertIsInstance(widget, forms.Select)
        self.assertEqual(widget.attrs["class"], "form-select")


class StateFieldTestCase(TestCase):
    """
    Test cases for the StateField
    """

    def test_state_field_without_data(self):
        """
        Test the Initialization of StateField before loading data to db.
        """
        field = StateField()
        self.assertEqual(field.choices[0][1], "Select a State from the dropdown")
        self.assertEqual(field.zones, [])
        self.assertEqual(field.empty_label, None)
        self.assertEqual(len(field.choices), 1)
        self.assertListEqual([("", "Select a State from the dropdown")], field.choices)
        with self.assertRaises(ValidationError):
            field.clean("Sokoto")
        widget = field.widget
        self.assertIsNone(widget.attrs.get("class", None))

    def test_state_field_initialization_with_data_and_kwargs(self):
        """
        Test the initialization of StateField with kwargs and data in db
        """
        load_fixtures()
        zone_names = [PoliticalZones.NORTH_CENTRAL, PoliticalZones.NORTH_WEST]
        field = StateField(
            label="Name of States",
            empty_label="Select a State",
            help_text="Select a state from the dropdown",
            zones=zone_names,
            widget=forms.Select(
                attrs={"class": "select form-select select2", "required": "required"}
            ),
        )
        self.assertEqual(field.label, "Name of States")
        self.assertEqual(field.empty_label, "Select a State")
        self.assertEqual(field.help_text, "Select a state from the dropdown")
        self.assertListEqual(field.zones, field.get_zones())
        states_in_zones = State.objects.filter(zone__name__in=zone_names).count()
        self.assertEqual(len(field.choices), states_in_zones + 1)
        self.assertIn(("Kano", "Kano"), field.choices)
        self.assertNotIn(("Togo", "Lome"), field.choices)
        with self.assertRaises(ValidationError):
            field.clean("Invalid State")
        self.assertListEqual(zone_names, field.get_zones())
        self.assertEqual(field.choices[0], ("", "Select a State"))

    def test_state_field_initialization_with_data_and_kwargs_no_zones(self):
        """
        Test the initialization of StateField with kwargs, and not zones after loading db
        """
        load_fixtures()
        with override_settings(DEFAULT_GEO_POLITICAL_ZONES=[]):
            field = StateField()
            self.assertEqual(len(field.choices), TOTAL_STATES + 1)
            first_three_choices = [choice[1] for choice in field.choices[1:4]]
            self.assertEqual(field.choices[1][0], FIRST_STATE)
            self.assertListEqual(sorted(FIRST_THREE_STATE), sorted(first_three_choices))
            self.assertEqual(field.choices[-1][0], LAST_STATE)
            last_three_choices = [choice[1] for choice in field.choices[-3:]]
            self.assertListEqual(sorted(last_three_choices), sorted(LAST_THREE_STATE))

    def test_state_field_widget(self):
        """
        Test state field widget
        """
        field = StateField(
            widget=forms.Select(
                attrs={"class": "select form-select select2", "required": "required"}
            ),
        )
        widget = field.widget
        self.assertIsInstance(widget, forms.Select)
        self.assertEqual(widget.attrs.get("class"), "select form-select select2")
        self.assertEqual(widget.attrs.get("required"), "required")


class LocalGovernmentFieldTestCases(TestCase):
    """
    Test cases for LocalGovernmentField
    """

    def test_local_government_field_without_data(self):
        """
        Test for the LocalGovernmentField initialization before loading data to db
        """
        field = LocalGovernmentField()
        self.assertIsNone(field.empty_label)
        self.assertEqual(field.zones, [])
        self.assertListEqual([("", "Select a LG")], field.choices)
        self.assertEqual(len(field.choices), 1)

    def test_local_government_field_with_kwargs_and_data(self):
        """
        Test for the LocalGovernmentField initialization with some kwargs, after loading data into db.
        """
        load_fixtures()
        with override_settings(DEFAULT_GEO_POLITICAL_ZONES=[]):
            field = LocalGovernmentField(
                label="Local Governments",
                help_text="Select a LGA from the dropdown",
                widget=forms.Select(
                    attrs={
                        "class": "select form-select select2",
                        "required": "required",
                    }
                ),
            )
            self.assertEqual(field.label, "Local Governments")
            self.assertEqual(field.help_text, "Select a LGA from the dropdown")
            self.assertIsInstance(field.zones, list)
            self.assertListEqual(
                sorted(field.get_zones()), sorted(PoliticalZones.values)
            )
            self.assertEqual(len(field.choices), TOTAL_LGAS + 1)
            self.assertEqual(field.choices[1][0], FIRST_LG)
            self.assertEqual(field.choices[-1][0], LAST_LG)

    def test_local_government_fields_with_kwargs_zones(self):
        """
        Test LocalGovernmentField initialization with kwargs zones only, no data
        """
        zone_names = [PoliticalZones.NORTH_CENTRAL, PoliticalZones.NORTH_WEST]
        field = LocalGovernmentField(zones=zone_names)
        lgs_in_zone = LocalGovernment.objects.filter(state__zone__name__in=zone_names)
        self.assertIsNotNone(field.zones)
        self.assertEqual(field.zones, zone_names)
        self.assertEqual(len(field.get_zones()), len(zone_names))
        self.assertEqual(len(field.choices), lgs_in_zone.count() + 1)
        self.assertEqual(field.choices[0], ("", "Select a LG"))
        with self.assertRaises(ValidationError):
            field.clean("Invalid LG")

    def test_local_government_widget_attrs(self):
        """
        Test the LocalGovernmentField widget
        """
        field = LocalGovernmentField(
            widget=forms.Select(
                attrs={"class": "select form-select select2", "required": "required"}
            )
        )
        widget = field.widget
        self.assertEqual(widget.attrs.get("class"), "select form-select select2")
        self.assertEqual(widget.attrs.get("required"), "required")
