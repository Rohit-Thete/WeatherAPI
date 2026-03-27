from rest_framework import serializers
from .models import MonthlyData,SeasonalData,AnnualData

class MonthlySerializer(serializers.ModelSerializer):
    class Meta:
        model=MonthlyData
        fields="__all__"


class SeasonalSerializer(serializers.ModelSerializer):
    class Meta:
        model=SeasonalData
        fields="__all__"


class AnnualSerializer(serializers.ModelSerializer):
    class Meta:
        model=AnnualData
        fields="__all__"