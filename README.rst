===============
Nigerian States
===============

Django Nigerian States is a comprehensive third-party Django application that provides a robust and efficient way to manage and interact with geopolitical data related to Nigeria. This application is designed to seamlessly integrate with your Django projects, providing pre-defined Django fields for all states, their capitals, local government areas, and geopolitical zones in Nigeria.
Installation
------------

Requirements
~~~~~~~~~~~~

- Python 3.10
- Django 5.0.1

Installation Steps
~~~~~~~~~~~~~~~~~~

1. Install Nigerian States using pip:

   .. code-block:: bash

      pip install django_nigerian_states

2. Add `'nigerian_states'` to `INSTALLED_APPS` in your Django project's settings.

3. Migrate your database:

   .. code-block:: bash

      python manage.py makemigrations
      python manage.py migrate

4. Load Fixtures:

   .. code-block:: bash

      python manage.py loaddata fixtures

Usage
-----

You can integrate Nigerian States into your Django forms seamlessly. Below is an example:

Example Usage
~~~~~~~~~~~~~

.. code-block:: python

    from django import forms
    from nigerian_states.fields import StateFormField, LocalGovernmentField

    class AboutForm(forms.ModelForm):
        zone = GeoPoliticalZoneField(
            label="Zone",
            help_text="Select a zone from the dropdown",
            widget=forms.Select(attrs={"class": "form-select"}),
        )
        state = StateField(
            label="Name of States",
            help_text="Select a state from the dropdown",
            widget=forms.Select(
                attrs={"class": "form-select", "required": "required"}
            ),
        )
        lga = LocalGovernmentField(
            label="Local Governments",
            help_text="Select a LGA from the dropdown",
            widget=forms.Select(
                attrs={"class": "form-select", "required": "required"}
            ),
        )

Configuration
-------------

You can configure Nigerian States by modifying your Django project `settings.py`:

.. code-block:: python

    DEFAULT_GEO_POLITICAL_ZONES = ["North Central", "North West"]

Setting `DEFAULT_GEO_POLITICAL_ZONES` restricts the choices for `(GeoPoliticalZoneField, StateField, or LocalGovernmentField)` to the specified zones.

You can also customize fields further by utilizing additional keyword arguments like `empty_label` and `zones`:

.. code-block:: python

    from django import forms
    from nigerian_states.fields import StateFormField, LocalGovernmentField
    from nigerian_states.enums import PoliticalZones

    zone = GeoPoliticalZoneField(
        label="Zone",
        empty_label="Select a GeoPolitical Zone",  # the first option in the dropdown
        zones=[PoliticalZones.SOUTH_EAST, PoliticalZones.SOUTH_EAST], # limits the field to specified political zones, overriding DEFAULT_GEO_POLITICAL_ZONES
    )

Note: In the above, by passing the `zones` kwargs in the field, It would override the `DEFAULT_GEO_POLITICAL_ZONES` set in the `settings.py`

Template Tags
-------------

To use the template tags, you need put ``{% load state_tags %}`` at the top of your django template.
The following template tags are available for use in your Django templates:

- ``{% get_states_in_zone ZONE_NAME %}``: Retrieves the list of states in a geopolitical zone.
- ``{% get_capital STATE_NAME %}``: Returns the capital of the state provided
- ``{% get_lgas_in_state STATE_NAME %}``: Retrieves the list of names of Local Government in the state.
- ``{% is_state_in_zone ZONE_NAME STATE_NAME %}``: Returns a boolean True if the state is from the GeoPolitical Zone.
- ``{% is_lga_in_state STATE_NAME LGA_NAME %}``: Returns a boolean True if the lga is from the state. else False
- ``{% default_zone %}``: Returns the default zone set in the settings.DEFAULT_GEO_POLITICAL_ZONES if set or empty list
- ``{% get_zone STATE_NAME %}``:Returns the name of the Zone which the state belongs to
- ``{% get_zone_info STATE_NAME %}``: Returns a dict of information about the state.


Contributing
------------

Contributions are welcomed and appreciated! Follow these steps to contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make changes, ensuring to write tests to confirm your changes did not break anything.
4. Push the changes to your fork.
5. Submit a pull request.

License
-------

This project is licensed under the MIT License - see the `LICENSE`_ file for details.

Developed by Afeez Lawal
~~~~~~~~~~~~~~~~~~~~~~~~~

Contact Me:
-----------

- Email: [Mail](mailto:lawalafeez052@gmail)
- Lawal Afeez: [LinkedIn:](https://www.linkedin.com/in/lawal-afeez/)
- Github: [Github:](https://github.com/Afeez31/)

.. _LICENSE: https://github.com/Afeez1131/LICENSE
