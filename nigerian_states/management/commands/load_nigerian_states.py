from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Run the fixtures to load data into DB"

    def handle(self, *args, **options):
        from django.core.management import call_command

        call_command("loaddata", "nigerian_states/fixtures/fixtures.json")
        self.stdout.write(self.style.SUCCESS("Completed loading data into DB"))
