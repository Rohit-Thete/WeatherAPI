from django.test import TestCase
from rest_framework.test import APIClient
from .models import MonthlyData

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

        print(response.data)
        self.assertEqual(response.status_code, 201)
        # self.assertEqual(response.data["region"],"India")
        # self.assertEqual(response.data["parameter"],"Tmin - celsius")
        self.assertEqual(MonthlyData.objects.count(), 1)
