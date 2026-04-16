from .constants import PARAMETER_UNITS
from .models import Unit, Parameter, Region, MonthlyData, SeasonalData, AnnualData


def get_parameter_obj(parameter_name):
    unit_name = PARAMETER_UNITS.get(parameter_name)
    unit_obj,_ = Unit.objects.get_or_create(name = unit_name)
    parameter_obj,created = Parameter.objects.get_or_create(name=parameter_name,defaults={"unit":unit_obj})

    if not created and parameter_obj.unit != unit_obj:
        parameter_obj.unit = unit_obj
        parameter_obj.save()

    return parameter_obj


def get_region_obj(region_name):
    region_obj, _ = Region.objects.get_or_create(name=region_name)
    return region_obj


def create_or_update_monthlydata(validated_data):
    region = get_region_obj(validated_data.get("region"))
    parameter = get_parameter_obj(validated_data.get("parameter"))

    obj,created = MonthlyData.objects.update_or_create(
        year = validated_data.get("year"),
        region = region,
        month = validated_data.get("month"),
        parameter = parameter,
        defaults = {"value":validated_data.get("value")}
    )

    return obj

def create_or_update_seasonaldata(validated_data):
    region = get_region_obj(validated_data.get("region"))
    parameter = get_parameter_obj(validated_data.get("region"))

    obj,created = SeasonalData.objects.update_or_create(
        year = validated_data.get("year"),
        region = region,
        season = validated_data.get("season"),
        parameter = parameter,
        defaults={"value":validated_data.get("value")}
    )
    return obj

def create_or_update_annualdata(validated_data):
    region = get_region_obj(validated_data.get("region"))
    parameter = get_parameter_obj(validated_data.get("parameter"))

    obj,created = AnnualData.objects.update_or_create(
        year = validated_data.get("year"),
        region = region,
        parameter = parameter,
        defaults={"value":validated_data.get("value")}
    )
