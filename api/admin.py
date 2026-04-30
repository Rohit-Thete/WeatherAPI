from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ["name"]



@admin.register(Parameter)
class ParameterAdmin(admin.ModelAdmin):
    list_display = ["name", "unit"]
    search_fields= ["name"]


@admin.register(MonthlyData)
class MonthlyAdmin(admin.ModelAdmin):
    list_display = ["year", "region", "month", "parameter", "value", "parameter__unit"]
    list_select_related = ["region","parameter"]
    ordering = ["-year"]
    list_filter = ["year", "month", "parameter", "region"]
    search_fields = ["year", "month", "parameter__name", "region__name"]
    # list_display_links = ["year","month"]
    list_per_page=50
    show_facets =admin.ShowFacets.ALWAYS
    radio_fields = {"month": admin.VERTICAL}
    autocomplete_fields=["region","parameter"]

    # def unit(self,obj):
    #     return obj.parameter.unit


@admin.register(SeasonalData)
class SeasonalAdmin(admin.ModelAdmin):
    list_display = ["year", "region", "season", "parameter", "value", "parameter__unit"]
    list_select_related = ["region","parameter"]
    ordering = ["-year"]
    list_filter = ["year", "season", "parameter", "region"]
    show_facets = admin.ShowFacets.ALWAYS
    search_fields = ["year", "season", "region__name", "parameter__name"]
    autocomplete_fields = ["region","parameter"]

    # def unit(self,obj):
    #     return obj.parameter.unit


@admin.register(AnnualData)
class AnnualAdmin(admin.ModelAdmin):
    list_display = ["year", "region", "parameter", "value", "parameter__unit"]
    list_select_related = ["region","parameter"]
    ordering = ["-year"]
    list_filter = ["year", "region", "parameter"]
    search_fields = ["year", "region__name", "parameter__name"]
    autocomplete_fields = ["region","parameter"]
    show_facets = admin.ShowFacets.ALWAYS

    # def unit(self,obj):
    #     return obj.parameter.unit