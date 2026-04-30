import django_filters

from .models import AnnualData, MonthlyData, SeasonalData


class MonthlyFilter(django_filters.FilterSet):
    region = django_filters.CharFilter(field_name="region__name")
    parameter = django_filters.CharFilter(field_name="parameter__name")

    class Meta:
        model = MonthlyData
        fields = ["year", "region", "parameter", "month"]


class SeasonalFilter(django_filters.FilterSet):
    region = django_filters.CharFilter(field_name="region__name")
    parameter = django_filters.CharFilter(field_name="parameter__name")

    class Meta:
        model = SeasonalData
        fields = ["year", "region", "parameter", "season"]


class AnnualFilter(django_filters.FilterSet):
    region = django_filters.CharFilter(field_name="region__name")
    parameter = django_filters.CharFilter(field_name="parameter__name")

    class Meta:
        model = AnnualData
        fields = ["year", "region", "parameter"]
