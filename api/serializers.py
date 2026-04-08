from rest_framework import serializers
from .models import MonthlyData,SeasonalData,AnnualData

class MonthlySerializer(serializers.ModelSerializer):
    year = serializers.IntegerField(source="year.year")
    region = serializers.CharField(source="region.name")
    parameter = serializers.CharField(source ="parameter.name")
    unit = serializers.CharField(source ="parameter.unit.name")

    class Meta:
        model=MonthlyData
        fields=["year","region","month","value","parameter","unit"]


class SeasonalSerializer(serializers.ModelSerializer):
    class Meta:
        model=SeasonalData
        fields="__all__"


class AnnualSerializer(serializers.ModelSerializer):
    class Meta:
        model=AnnualData
        fields="__all__"