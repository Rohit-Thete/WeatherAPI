from django.core.management.base import BaseCommand
from api.utils import load_data
from api.models import MonthlyData, SeasonalData, AnnualData

REGIONS = [
    "UK",
    "England",
    "Scotland",
    "Wales",
    "Northern_Ireland",
    "England_and_Wales",
]
PARAMETERS = ["Tmax", "Tmin", "Sunshine", "Rainfall"]


class Command(BaseCommand):
    help = "Load weather data for all regions and parameters"

    def handle(self, *args, **kwargs):

        if (
            MonthlyData.objects.exists()
            or SeasonalData.objects.exists()
            or AnnualData.objects.exists()
        ):
            self.stdout.write(self.style.WARNING("Data already exists skipping..."))
            return

        total = len(REGIONS) * len(PARAMETERS)
        count = 0

        for region in REGIONS:
            for parameter in PARAMETERS:
                try:
                    load_data(region, parameter)
                    count += 1
                    self.stdout.write(
                        f"[{count}/{total}] Loaded {region} - {parameter}"
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f"Failed {region} - {parameter}: {str(e)}")
                    )

        self.stdout.write(
            self.style.SUCCESS(f"Done! Loaded {count}/{total} successfully.")
        )
