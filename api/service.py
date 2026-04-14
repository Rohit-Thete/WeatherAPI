from .constants import PARAMETER_UNITS
from .models import Unit, Parameter, Region


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

