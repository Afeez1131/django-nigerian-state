from django.db import models
from nigerian_states.enums import PoliticalZones


class GeoPoliticalZone(models.Model):
    name = models.CharField(max_length=55, choices=PoliticalZones.choices)

    def __str__(self):
        return self.name

    @property
    def all_states(self):
        return self.states.all()

    @property
    def total_states(self):
        return self.all_states.count()

    @property
    def all_lgas(self):
        return LocalGovernment.objects.filter(state__in=self.all_states)

    @property
    def total_lgas(self):
        return self.all_lgas.count()


class State(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    capital = models.CharField(max_length=100)
    zone = models.ForeignKey(
        GeoPoliticalZone, on_delete=models.CASCADE, related_name="states"
    )

    def __str__(self):
        return self.name

    @property
    def total_lgas(self):
        return self.localgovernment_set.count()

    @property
    def lgas(self):
        return self.localgovernment_set.all()


class LocalGovernment(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return f"{self.state.name}: {self.name}"
