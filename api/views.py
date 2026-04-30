from django.shortcuts import render
from .filters import MonthlyFilter, SeasonalFilter, AnnualFilter
from .models import MonthlyData, SeasonalData, AnnualData
from .serializers import (
    MonthlySerializer,
    SeasonalSerializer,
    AnnualSerializer,
    MonthlyWriteSerializer,
    SeasonalWriteSerializer,
    AnnualWriteSerializer,
)
from rest_framework import viewsets
from rest_framework.views import APIView
from .constants import REGIONS, PARAMETERS
from .utils import load_data
from rest_framework.response import Response


class LoadData(APIView):
    def post(self, request):

        try:
            if (
                MonthlyData.objects.count() == 0
                and SeasonalData.objects.count() == 0
                and AnnualData.objects.count() == 0
            ):
                for i in REGIONS:
                    for j in PARAMETERS:
                        load_data(i, j)

                return Response("data Loaded Successfully", status=201)

        except Exception as e:
            return Response({"error": str(e)}, status=500)


class MonthlyViewSet(viewsets.ModelViewSet):
    queryset = MonthlyData.objects.select_related("region", "parameter__unit")
    filterset_class = MonthlyFilter

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return MonthlySerializer
        return MonthlyWriteSerializer


class SeasonalViewSet(viewsets.ModelViewSet):
    queryset = SeasonalData.objects.select_related("region", "parameter__unit")
    filterset_class = SeasonalFilter

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return SeasonalSerializer
        return SeasonalWriteSerializer


class AnnualViewSet(viewsets.ModelViewSet):
    queryset = AnnualData.objects.select_related("region", "parameter__unit")
    filterset_class = AnnualFilter

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return AnnualSerializer
        return AnnualWriteSerializer


def home(request):
    return render(request, "index.html")
