from django.shortcuts import render
from .models import MonthlyData, SeasonalData, AnnualData,Unit,Year,Parameter,Region
from .serializers import MonthlySerializer, SeasonalSerializer, AnnualSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .utils import load_data
from rest_framework import status
from .constants import PARAMETER_CHOICES,SEASON_CHOICES,MONTH_CHOICES,UNITS,PARAMETER_UNITS

REGIONS = ["UK", "England", "Scotland", "Wales", "Northern_Ireland", "England_and_Wales"]
PARAMETERS = ["Tmax", "Tmin", "Sunshine", "Rainfall"]


if MonthlyData.objects.count() == 0 and SeasonalData.objects.count() == 0 and AnnualData.objects.count() == 0:
    for i in REGIONS:
        for j in PARAMETERS:
            load_data(i, j)


def apply_filter(queryset, field, value):
    if value:
        if not queryset.filter(**{field: value}).exists():
            return None, Response(
                {"error": f"Data for {field} = {value} is not present"},
                status=404
            )
        return queryset.filter(**{field: value}), None
    return queryset, None



class MonthlyView(APIView):
    def get(self, request, **kwargs):
        data = MonthlyData.objects.all()
        filters = {
            "year":            request.GET.get('year'),
            "parameter__name": request.GET.get('parameter'),
            "region__name":    kwargs.get('region') or request.GET.get('region'),
            "month":           request.GET.get('month'),
        }
        for field, value in filters.items():
            data, error = apply_filter(data, field, value)
            if error:
                return error
            serializer = MonthlySerializer(data, many=True).data
        return Response(serializer)
    
    def post(self,request):
        data = request.data 
        year_value =data.get("year")
        month_value = data.get("month")
        region_value = data.get("region")
        parameter_name = data.get("parameter")
        value = data.get("value")

        if not all(["year","month","region","parameter","value"]):
            return Response ("All values are required")
        
        valid_parameters =[p[0] for p in PARAMETER_CHOICES]
        if parameter_name not in valid_parameters:
            return Response("Enter valid Parameter")
        
        valid_months =[m[0] for m in MONTH_CHOICES]
        if month_value not in valid_months:
            return Response("Invalid Month")
        

        unit_name = PARAMETER_UNITS.get(parameter_name)

        unit_obj,_ = Unit.objects.get_or_create(name = unit_name)

        parameter_obj,c = Parameter.objects.get_or_create(name = parameter_name,defaults={"unit":unit_obj})

        if not c and parameter_obj.unit != unit_obj:
            parameter_obj.unit=unit_obj
            parameter_obj.save()

        year_obj, _ = Year.objects.get_or_create(year = year_value)
        region_obj, _ = Region.objects.get_or_create(name=region_value)

        if value is not None:
            obj,created = MonthlyData.objects.get_or_create(
                year = year_obj,
                region=region_obj,
                month=month_value,
                parameter = parameter_obj,
                value=value

            )

        serializer = MonthlySerializer(obj)
        
        return Response(serializer.data,
                        status = 201 if created else 200
                        )



              


class SeasonalView(APIView):
    def get(self, request, **kwargs):
        data = SeasonalData.objects.all()
        filters = {
            "year":            request.GET.get('year'),
            "parameter__name": request.GET.get('parameter'),
            "region__name":    kwargs.get('region') or request.GET.get('region'),
            "season":          request.GET.get('season'),
        }
        for field, value in filters.items():
            data, error = apply_filter(data, field, value)
            if error:
                return error
            serializer = SeasonalSerializer(data, many=True)
        return Response(serializer.data)
    

    def post(self,request):
        data = request.data
        year_value = data.get("year")
        region_value = data.get("region")
        season_value = data.get("season")
        parameter_name = data.get("parameter")
        value = data.get("value")

        valid_season = [s[0] for s in SEASON_CHOICES]
        if season_value not in valid_season:
            return Response(
                {"error":"Enter Valid Season"},
                status=400
            )
        
        unit_name = PARAMETER_UNITS.get(parameter_name)
        unit_obj, _= Unit.objects.get_or_create(name = unit_name)

        valid_parameters = [p[0] for p in PARAMETER_CHOICES]
        if parameter_name not in valid_parameters:
            return Response({
                "error":"Enter Valid Parameter Value"},
                status=400
            )
        parameter_obj,c = Parameter.objects.get_or_create(name = parameter_name,defaults={"unit":unit_obj})

        if not c and parameter_obj.unit != unit_obj:
            parameter_obj.unit = unit_obj
            parameter_obj.save()

        year_obj,_ = Year.objects.get_or_create(year=year_value)

        region_obj,_ = Region.objects.get_or_create(name = region_value)

        if value is not None:
            obj,created = SeasonalData.objects.get_or_create(
                year = year_obj,
                region = region_obj,
                season = season_value,
                parameter = parameter_obj,
                value = value
            )

        serializer = SeasonalSerializer(obj)

        return Response(serializer.data,
                        status=201 if created else 200
                        )

        

class AnnualView(APIView):
    def get(self, request, **kwargs):
        data = AnnualData.objects.all()
        filters = {
            "year":            request.GET.get('year'),
            "parameter__name": request.GET.get('parameter'),
            "region__name":    kwargs.get('region') or request.GET.get('region'),
        }
        for field, value in filters.items():
            data, error = apply_filter(data, field, value)
            if error:
                return error
        return Response(AnnualSerializer(data, many=True).data)
    

    def post(self,request):
        data = request.data

        year_value = data.get("year")
        region_value = data.get("region")
        parameter_name = data.get("parameter")
        value = data.get("value")

        unit_name = PARAMETER_UNITS.get(parameter_name)
        unit_obj,_ = Unit.objects.get_or_create(name = unit_name)

        valid_parameters =[p[0] for p in PARAMETER_CHOICES]
        if parameter_name not in valid_parameters:
            return Response(
                {
                    "error":"Enter Valid Parameter"
                },
                status=400
            )
        
        parameter_obj ,c =Parameter.objects.get_or_create(name = parameter_name,defaults={"unit":unit_obj})

        if not c and parameter_obj.unit != unit_obj:
            parameter_obj.unit = unit_obj
            parameter_obj.save()

        year_obj,_ = Year.objects.get_or_create(year = year_value)

        region_obj, _ = Region.objects.get_or_create(name = region_value)

        if value is not None:
            obj,created = AnnualData.objects.get_or_create(
                year = year_obj,
                region = region_obj,
                parameter = parameter_obj,
                value = value
            )

        serializer = AnnualSerializer(obj)

        return Response(
            serializer.data,
            status=201 if created else 200
        )





def home(request):
    return render(request, 'index.html')