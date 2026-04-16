from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display=["name"]

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display=["name"]

@admin.register(Parameter)
class ParameterAdmin(admin.ModelAdmin):
    list_display=["name","unit"]

@admin.register(MonthlyData)
class MonthlyAdmin(admin.ModelAdmin):
    list_display = ["year", "region", "month", "parameter", "value", "parameter__unit"]
    ordering = ["-year"]
    list_filter = ["year", "month", "parameter", "region"]
    search_fields = ["year", "month", "parameter__name", "region__name"]


@admin.register(SeasonalData)
class SeasonalAdmin(admin.ModelAdmin):
    list_display = ["year", "region", "season", "parameter", "value", "parameter__unit"]
    ordering = ["-year"]
    list_filter = ["year", "season", "parameter", "region"]
    search_fields = ["year", "season", "region__name", "parameter__name"]


@admin.register(AnnualData)
class AnnualAdmin(admin.ModelAdmin):
    list_display = ["year", "region", "parameter", "value", "parameter__unit"]
    ordering = ["-year"]
    list_filter = ["year", "region", "parameter"]
    search_fields = ["year", "region__name", "parameter__name"]
