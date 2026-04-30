from django.test import TestCase
from rest_framework.test import APIClient
from .models import AnnualData, MonthlyData, SeasonalData
from .service import get_or_create_parameter_obj, get_or_create_region_obj

# Create your tests here.


class MonthlyTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.valid_data = {
            "year": 2026,
            "region": "India",
            "month": "february",
            "parameter": "Tmin",
            "value": 36.37,
        }

    def test_create_monthly_data(self):

        response = self.client.post("/monthly/", self.valid_data)

        self.assertEqual(response.status_code, 201)
        # self.assertEqual(response.data["region"],"India")
        # self.assertEqual(response.data["parameter"],"Tmin - celsius")
        self.assertEqual(MonthlyData.objects.count(), 1)

    def test_list_monthly_data_with_filters(self):
        region = get_or_create_region_obj("England")
        parameter = get_or_create_parameter_obj("Tmax")

        MonthlyData.objects.create(
            year=2024,
            region=region,
            month="january",
            parameter=parameter,
            value=8.5,
        )
        MonthlyData.objects.create(
            year=2024,
            region=region,
            month="february",
            parameter=parameter,
            value=9.0,
        )

        response = self.client.get("/monthly/?year=2024&region=England&month=january")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["month"], "january")

    def test_list_monthly_data_filters_by_region_query_param(self):
        england = get_or_create_region_obj("England")
        scotland = get_or_create_region_obj("Scotland")
        parameter = get_or_create_parameter_obj("Tmax")

        MonthlyData.objects.create(
            year=2024,
            region=england,
            month="january",
            parameter=parameter,
            value=8.5,
        )
        MonthlyData.objects.create(
            year=2024,
            region=scotland,
            month="january",
            parameter=parameter,
            value=4.0,
        )

        response = self.client.get("/monthly/?region=England")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["region"], "England")


class SeasonalAndAnnualFilterTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.region = get_or_create_region_obj("Scotland")
        self.parameter = get_or_create_parameter_obj("Rainfall")

    def test_list_seasonal_data_with_filters(self):
        SeasonalData.objects.create(
            year=2023,
            region=self.region,
            season="winter",
            parameter=self.parameter,
            value=100.0,
        )
        SeasonalData.objects.create(
            year=2023,
            region=self.region,
            season="summer",
            parameter=self.parameter,
            value=55.0,
        )

        response = self.client.get(
            "/seasonal/?year=2023&region=Scotland&parameter=Rainfall&season=winter"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["season"], "winter")

    def test_list_annual_data_with_filters(self):
        AnnualData.objects.create(
            year=2022,
            region=self.region,
            parameter=self.parameter,
            value=750.0,
        )
        AnnualData.objects.create(
            year=2021,
            region=self.region,
            parameter=self.parameter,
            value=700.0,
        )

        response = self.client.get(
            "/annual/?year=2022&region=Scotland&parameter=Rainfall"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["year"], 2022)

    def test_list_annual_data_filters_by_parameter_query_param(self):
        other_parameter = get_or_create_parameter_obj("Sunshine")

        AnnualData.objects.create(
            year=2022,
            region=self.region,
            parameter=self.parameter,
            value=750.0,
        )
        AnnualData.objects.create(
            year=2022,
            region=self.region,
            parameter=other_parameter,
            value=120.0,
        )

        response = self.client.get("/annual/?parameter=Rainfall")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["parameter"], "Rainfall")
