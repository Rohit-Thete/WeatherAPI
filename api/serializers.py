from rest_framework import serializers
from .models import MonthlyData, SeasonalData, AnnualData, Region, Parameter, Unit
from .constants import MONTH_CHOICES, PARAMETER_CHOICES, SEASON_CHOICES, PARAMETER_UNITS
from .service import get_parameter_obj, get_region_obj


class MonthlySerializer(serializers.ModelSerializer):
    region = serializers.CharField(source="region.name")
    parameter = serializers.CharField(source="parameter.name")
    unit = serializers.CharField(source="parameter.unit.name")

    class Meta:
        model = MonthlyData
        fields = ["year", "region", "month", "value", "parameter", "unit"]


class monthlyWriteSerializer(serializers.ModelSerializer):
    region = serializers.CharField()
    parameter = serializers.CharField()

    class Meta:
        model = MonthlyData
        fields = ["year", "region", "month", "parameter", "value"]

    def validate(self, data):

        month = data.get("month")
        if month is not None and month not in [m[0] for m in MONTH_CHOICES]:
            raise serializers.ValidationError(
                {"month":f"enter valid Month from {MONTH_CHOICES}"}
            )

        parameter = data.get("parameter")
        if parameter is not None and parameter not in [p[0] for p in PARAMETER_CHOICES]:
            raise serializers.ValidationError(
                {"parameter":f"enter valid parameter from {PARAMETER_CHOICES}"}
            )

        return data

    def create(self, validated_data):

        from .service import create_or_update_monthlydata

        return create_or_update_monthlydata(validated_data)
        # month_value = validated_data.get("month")
        # value = validated_data.get("value")
        # year = validated_data.get("year")
        # region_name = validated_data.get("region")

        # region_obj = get_region_obj(region_name)

        # parameter_name = validated_data.get("parameter")
        # parameter_obj = get_parameter_obj(parameter_name)
        # # unit_name = PARAMETER_UNITS.get(parameter_name)
        # # unit_obj, _ = Unit.objects.get_or_create(name=unit_name)

        # # parameter_obj, c = Parameter.objects.get_or_create(
        # #     name=parameter_name, defaults={"unit": unit_obj}
        # # )

        # # if not c and parameter_obj.unit != unit_obj:
        # #     parameter_obj.unit = unit_obj
        # #     parameter_obj.save()

        # obj, _ = MonthlyData.objects.update_or_create(
        #     year=year,
        #     region=region_obj,
        #     month=month_value,
        #     parameter=parameter_obj,
        #     defaults={"value":value}
        # )

        # return obj

    def update(self, instance, validated_data):

        from .service import update_monthly_data

        return update_monthly_data(instance,validated_data)

        # if "region" in validated_data:
        #     region_obj, _ = Region.objects.get_or_create(
        #         name=validated_data.get("region")
        #     )
        #     instance.region = region_obj

        # if "parameter" in validated_data:
        #     parameter_name = validated_data.get("parameter")
        #     unit_name = PARAMETER_UNITS.get(parameter_name)
        #     unit_obj, _ = Unit.objects.get_or_create(name=unit_name)
        #     parameter_obj, created = Parameter.objects.get_or_create(
        #         name=parameter_name, defaults={"unit": unit_obj}
        #     )

        #     if not created and parameter_obj.unit != unit_obj:
        #         parameter_obj.unit = unit_obj
        #         parameter_obj.save()

        #     instance.parameter = parameter_obj

        # instance.year = validated_data.get("year", instance.year)
        # instance.month = validated_data.get("month", instance.month)
        # instance.value = validated_data.get("value", instance.value)

        # instance.save()

        # return instance


class SeasonalSerializer(serializers.ModelSerializer):
    region = serializers.CharField(source="region.name")
    parameter = serializers.CharField(source="parameter.name")
    unit = serializers.CharField(source="parameter.unit.name")

    class Meta:
        model = SeasonalData
        fields = ["year", "region", "season", "value", "parameter", "unit"]


class SeasonalWriteSerializer(serializers.ModelSerializer):
    region = serializers.CharField()
    parameter = serializers.CharField()

    class Meta:
        model = SeasonalData
        fields = ["year", "region", "season", "value", "parameter"]

    def validate(self, data):

        season = data.get("season")
        if season is not None and season not in [s[0] for s in SEASON_CHOICES]:
            raise serializers.ValidationError(
                {"season":f"enter valid Season from {SEASON_CHOICES}"}
            )

        parameter = data.get("parameter")
        if parameter is not None and parameter not in [p[0] for p in PARAMETER_CHOICES]:
            raise serializers.ValidationError(
                {"parameter":f"enter valid parameter from {PARAMETER_CHOICES}"}
            )

        return data

    def create(self, validated_data):

        from .service import create_or_update_seasonaldata

        return create_or_update_seasonaldata(validated_data)

        # year = validated_data.get("year")
        # season_name = validated_data.get("season")
        # parameter_name = validated_data.get("parameter")
        # value = validated_data.get("value")
        # region_name = validated_data.get("region")

        # region_obj = get_region_obj(region_name)
        # parameter_obj = get_parameter_obj(parameter_name)
        # # unit_name = PARAMETER_UNITS.get(parameter_name)
        # # unit_obj, _ = Unit.objects.get_or_create(name=unit_name)

        # # parameter_obj, created = Parameter.objects.get_or_create(
        # #     name=parameter_name, defaults={"unit": unit_obj}
        # # )

        # # if not created and parameter_obj.unit != unit_obj:
        # #     parameter_obj.unit = unit_obj
        # #     parameter_obj.save()

        # obj, _ = SeasonalData.objects.update_or_create(
        #     year=year,
        #     region=region_obj,
        #     season=season_name,
        #     parameter=parameter_obj,
        #    defaults={"value":value}
        # )

        # return obj

    def update(self, instance, validated_data):
        from .service import update_seasonal_data

        return update_seasonal_data(instance,validated_data)


class AnnualSerializer(serializers.ModelSerializer):
    region = serializers.CharField(source="region.name")
    parameter = serializers.CharField(source="parameter.name")
    unit = serializers.CharField(source="parameter.unit.name")

    class Meta:
        model = AnnualData
        fields = ["year", "region", "value", "parameter", "unit"]


class AnnualWriteSerializer(serializers.ModelSerializer):
    region = serializers.CharField()
    parameter = serializers.CharField()

    class Meta:
        model = AnnualData
        fields = ["year", "region", "parameter", "value"]

    def validate(self, data):

        parameter = data.get("parameter")
        if parameter is not None and parameter not in [p[0] for p in PARAMETER_CHOICES]:
            raise serializers.ValidationError(
                {"parameter":f"enter valid parameter from {PARAMETER_CHOICES}"}
            )

        return data

    def create(self, validated_data):

        from .service import create_or_update_annualdata

        return create_or_update_annualdata(validated_data)

        # year = validated_data.get("year")
        # value = validated_data.get("value")
        # parameter_name = validated_data.get("parameter")
        # region_name = validated_data.get("region")

        # parameter_obj = get_parameter_obj(parameter_name)
        # region_obj = get_region_obj(region_name)

        # obj, _ = AnnualData.objects.update_or_create(
        #     year=year, region=region_obj, parameter=parameter_obj, defaults={"value":value}
        # )

        # return obj

    def update(self, instance, validated_data):
        from .service import update_annual_data

        return update_annual_data(instance,validated_data)
