import threading
import os
from django.apps import AppConfig


class ApiConfig(AppConfig):
    name = "api"

    def ready(self):
        # prevents running twice due to Django autoreloader
        if os.environ.get("RUN_MAIN") == "true":
            thread = threading.Thread(target=self._load_data)
            thread.daemon = True
            thread.start()

    def _load_data(self):
        from .models import MonthlyData, SeasonalData, AnnualData
        from .utils import load_data

        REGIONS = [
            "UK",
            "England",
            "Scotland",
            "Wales",
            "Northern_Ireland",
            "England_and_Wales",
        ]
        PARAMETERS = ["Tmax", "Tmin", "Sunshine", "Rainfall"]

        if (
            MonthlyData.objects.exists()
            or SeasonalData.objects.exists()
            or AnnualData.objects.exists()
        ):
            print("Data already exists, skipping...")
            return

        print("Loading data...")

        for region in REGIONS:
            for parameter in PARAMETERS:
                load_data(region, parameter)
                print(f"Loaded {region} - {parameter}")

        print("All data loaded successfully!")
