from rest_framework import serializers
from .models import MonthlyData,SeasonalData,AnnualData,Region,Parameter,Unit,Year
from .constants import MONTH_CHOICES,PARAMETER_CHOICES,SEASON_CHOICES,PARAMETER_UNITS

class MonthlySerializer(serializers.ModelSerializer):
    year = serializers.IntegerField(source="year.year")
    region = serializers.CharField(source="region.name")
    parameter = serializers.CharField(source ="parameter.name")
    unit = serializers.CharField(source ="parameter.unit.name")

    class Meta:
        model=MonthlyData
        fields=["year","region","month","value","parameter","unit"]


class monthlyWriteSerializer(serializers.ModelSerializer):
    year = serializers.IntegerField()
    region=serializers.CharField()
    parameter = serializers.CharField()

    class Meta:
        model = MonthlyData
        fields=["year","region","month","parameter","value"]

    def validate(self,data):

        if data["month"] not in [m[0] for m in MONTH_CHOICES]:
            raise serializers.ValidationError("Enter valid month")
        
        if data["parameter"] not in [p[0] for p in PARAMETER_CHOICES]:
            raise serializers.ValidationError("enter valid parameter")
        
        return data
    
    
    def create(self,validated_data):
        month_value = validated_data["month"]
        value = validated_data["value"]
       
        region_obj, _= Region.objects.get_or_create(name=validated_data["region"])
        year_obj, _ = Year.objects.get_or_create(year = validated_data["year"])

        parameter_name = validated_data("parameter")
        unit_name = PARAMETER_UNITS.get(parameter_name)
        unit_obj,_ =Unit.objects.get_or_create(name=unit_name)

        parameter_obj,c = Parameter.objects.get_or_create(name = parameter_name,defaults={"unit":unit_obj})

        if not c and parameter_obj.unit != unit_obj:
            parameter_obj.unit = unit_obj
            parameter_obj.save()

        obj,_ = MonthlyData.objects.get_or_create(
            year = year_obj,
            region = region_obj,
            month = month_value,
            parameter = parameter_obj,
            value = value
        )

        return obj


        

        

        




class SeasonalSerializer(serializers.ModelSerializer):
    class Meta:
        model=SeasonalData
        fields="__all__"


class AnnualSerializer(serializers.ModelSerializer):
    class Meta:
        model=AnnualData
        fields="__all__"