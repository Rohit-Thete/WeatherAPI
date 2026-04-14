from django.shortcuts import render
from .models import MonthlyData, SeasonalData, AnnualData, Unit, Parameter, Region
from .serializers import (
    MonthlySerializer,
    SeasonalSerializer,
    AnnualSerializer,
    monthlyWriteSerializer,
    SeasonalWriteSerializer,
    AnnualWriteSerializer,
)
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
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


def apply_filter(queryset, field, value):
    if value:
        if not queryset.filter(**{field: value}).exists():
            return None, Response(
                {"error": f"Data for {field} = {value} is not present"}, status=404
            )
        return queryset.filter(**{field: value}), None
    return queryset, None


# class LoadData(APIView):
#     def post(self, request):

#         try:
#             if (
#                 MonthlyData.objects.count() == 0
#                 and SeasonalData.objects.count() == 0
#                 and AnnualData.objects.count() == 0
#             ):
#                 for i in REGIONS:
#                     for j in PARAMETERS:
#                         load_data(i, j)

#                 return Response("data Loaded Successfully", status=201)

#         except Exception as e:
#             return Response({"error": str(e)}, status=500)


class MonthlyViewSet(viewsets.ModelViewSet):
    queryset = MonthlyData.objects.select_related("region", "parameter__unit")
    
    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return MonthlySerializer
        return monthlyWriteSerializer


class SeasonalViewSet(viewsets.ModelViewSet):
    queryset = SeasonalData.objects.select_related("region", "parameter__unit")
    
    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return SeasonalSerializer
        return SeasonalWriteSerializer


class AnnualViewSet(viewsets.ModelViewSet):
    queryset = AnnualData.objects.select_related("region", "parameter__unit")
    
    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return AnnualSerializer
        return AnnualWriteSerializer

def home(request):
    return render(request, "index.html")
