from django.core.management.base import BaseCommand
from bilanz.models import Ort


class Command(BaseCommand):
    help = 'Lädt Klimadaten für deutsche Städte'

    def handle(self, *args, **options):
        klimadaten = [
            {
                'name': 'München',
                'temperatur_mittel': 9.1,
                'heizgradtage': 3500,
                'solarstrahlung_nord': 300,
                'solarstrahlung_sued': 1100,
                'solarstrahlung_ost': 700,
                'solarstrahlung_west': 700,
                'solarstrahlung_horizontal': 1000,
            },
            {
                'name': 'Berlin',
                'temperatur_mittel': 9.6,
                'heizgradtage': 3200,
                'solarstrahlung_nord': 280,
                'solarstrahlung_sued': 1050,
                'solarstrahlung_ost': 680,
                'solarstrahlung_west': 680,
                'solarstrahlung_horizontal': 950,
            },
            {
                'name': 'Hamburg',
                'temperatur_mittel': 9.1,
                'heizgradtage': 3300,
                'solarstrahlung_nord': 270,
                'solarstrahlung_sued': 1000,
                'solarstrahlung_ost': 650,
                'solarstrahlung_west': 650,
                'solarstrahlung_horizontal': 900,
            },
            {
                'name': 'Köln',
                'temperatur_mittel': 10.3,
                'heizgradtage': 3000,
                'solarstrahlung_nord': 290,
                'solarstrahlung_sued': 1080,
                'solarstrahlung_ost': 690,
                'solarstrahlung_west': 690,
                'solarstrahlung_horizontal': 980,
            },
            {
                'name': 'Frankfurt',
                'temperatur_mittel': 10.6,
                'heizgradtage': 2900,
                'solarstrahlung_nord': 300,
                'solarstrahlung_sued': 1120,
                'solarstrahlung_ost': 710,
                'solarstrahlung_west': 710,
                'solarstrahlung_horizontal': 1020,
            },
            {
                'name': 'Stuttgart',
                'temperatur_mittel': 9.3,
                'heizgradtage': 3400,
                'solarstrahlung_nord': 310,
                'solarstrahlung_sued': 1150,
                'solarstrahlung_ost': 720,
                'solarstrahlung_west': 720,
                'solarstrahlung_horizontal': 1050,
            },
        ]

        for daten in klimadaten:
            ort, created = Ort.objects.get_or_create(
                name=daten['name'],
                defaults=daten
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Ort "{ort.name}" erstellt')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Ort "{ort.name}" existiert bereits')
                )

        self.stdout.write(
            self.style.SUCCESS('Klimadaten erfolgreich geladen')
        )