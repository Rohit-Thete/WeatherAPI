from rest_framework import serializers
from .models import MonthlyData,SeasonalData,AnnualData,Region,Parameter,Unit
from .constants import MONTH_CHOICES,PARAMETER_CHOICES,SEASON_CHOICES,PARAMETER_UNITS

class MonthlySerializer(serializers.ModelSerializer):
    region = serializers.CharField(source="region.name")
    parameter = serializers.CharField(source ="parameter.name")
    unit = serializers.CharField(source ="parameter.unit.name")

    class Meta:
        model=MonthlyData
        fields=["year","region","month","value","parameter","unit"]


class monthlyWriteSerializer(serializers.ModelSerializer):
    region=serializers.CharField()
    parameter = serializers.CharField()

    class Meta:
        model = MonthlyData
        fields=["year","region","month","parameter","value"]

    def validate(self,data):

        if data.get("month") not in [m[0] for m in MONTH_CHOICES]:
            raise serializers.ValidationError("Enter valid month")
        
        if data.get("parameter") not in [p[0] for p in PARAMETER_CHOICES]:
            raise serializers.ValidationError("enter valid parameter")
        
        return data
    
    
    def create(self,validated_data):
        month_value = validated_data.get("month")
        value = validated_data.get("value")
        year = validated_data.get("year")
       
        region_obj, _= Region.objects.get_or_create(name=validated_data.get("region"))
        

        parameter_name = validated_data.get("parameter")
        unit_name = PARAMETER_UNITS.get(parameter_name)
        unit_obj,_ =Unit.objects.get_or_create(name=unit_name)

        parameter_obj,c = Parameter.objects.get_or_create(name = parameter_name,defaults={"unit":unit_obj})

        if not c and parameter_obj.unit != unit_obj:
            parameter_obj.unit = unit_obj
            parameter_obj.save()

        obj,_ = MonthlyData.objects.get_or_create(
            year = year,
            region = region_obj,
            month = month_value,
            parameter = parameter_obj,
            value = value
        )

        return obj




class SeasonalSerializer(serializers.ModelSerializer):
    region = serializers.CharField(source="region.name")
    parameter = serializers.CharField(source = "parameter.name")
    unit = serializers.CharField(source = "parameter.unit.name")
    class Meta:
        model=SeasonalData
        fields=["year","region","season","value","parameter","unit"]

class SeasonalWriteSerializer(serializers.ModelSerializer):
    region = serializers.CharField()
    parameter = serializers.CharField()

    class Meta:
        model = SeasonalData
        fields=["year","region","season","value","parameter"]

    def validate(self, data):

        if data.get("season") not in [s[0] for s in SEASON_CHOICES]:
            raise serializers.ValidationError("Enter valid Season")
        
        if data.get("parameter") not in [p[0] for p in PARAMETER_CHOICES]:
            raise serializers.ValidationError("enter valid parameter")
        
        return data
    
    
    def create(self, validated_data):
        
        year = validated_data.get("year")
        season_name = validated_data.get("season")
        parameter_name = validated_data.get("parameter")
        value = validated_data.get("value")

        region_obj,_ = Region.objects.get_or_create(name = validated_data.get("region"))
        unit_name = PARAMETER_UNITS.get(parameter_name)
        unit_obj ,_= Unit.objects.get_or_create(name = unit_name)

        parameter_obj,created = Parameter.objects.get_or_create(name = parameter_name,defaults={"unit":unit_obj})

        if not created and parameter_obj.unit not in unit_obj:
            parameter_obj.unit = unit_obj
            parameter_obj.save()

        
        obj,_ = SeasonalData.objects.get_or_create(
            year = year,
            region = region_obj,
            season = season_name,
            parameter = parameter_obj,
            value = value
        )

        return obj



        
    

        

class AnnualSerializer(serializers.ModelSerializer):
    class Meta:
        model=AnnualData
        fields="__all__"