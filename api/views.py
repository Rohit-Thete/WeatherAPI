from django.shortcuts import render
from .models import MonthlyData,SeasonalData,AnnualData
from .serializers import MonthlySerializer,SeasonalSerializer,AnnualSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from .utils import load_data, get_monthly_filtered_data, get_seasonal_filtered_data, get_annual_filtered_data

region=["UK","England","Scotland","Wales","Northern Ireland","England & Wales"]
parameter=["Tmax","Tmin","Sunshine","Rainfall"]
# MonthlyData.objects.all().delete()
# SeasonalData.objects.all().delete()
# AnnualData.objects.all().delete()
if MonthlyData.objects.count() == 0 and SeasonalData.objects.count() == 0 and AnnualData.objects.count() == 0 :
    for i in region:
        for j in parameter:
            load_data(i,j)

    # load_data("UK", "Tmax")
    # load_data("UK", "Tmin")

    # load_data("England", "Tmax")
    # load_data("England", "Tmin")

    # load_data("Scotland", "Tmax")

# Create your views here.

class MonthlyView(APIView):
    def get(self,request):
        data = MonthlyData.objects.all()

        year = request.GET.get('year')
        parameter=request.GET.get('parameter')
        region = request.GET.get('region')
        month = request.GET.get('month')

        data = get_monthly_filtered_data(year,parameter,region,month)

        serializer=MonthlySerializer(data,many=True)

        return Response(serializer.data)
    
class SeasonalView(APIView):
    def get(self,request):
        data = SeasonalData.objects.all()

        abc = SeasonalData.objects.values_list('region',flat=True).distinct()
        print(abc)

        year=request.GET.get('year')
        parameter=request.GET.get('parameter')
        region=request.GET.get('region')
        season=request.GET.get('season')
 

        data = get_seasonal_filtered_data(year,parameter,region,season)

        # if year and season:
        #     data = data.filter(year=year,season=season)

        # if year and region:
        #     data = data.filter(year=year,region=region)

        # if region and season:
        #     data = data.filter(region=region,season=season)

         # if year or parameter:
        #     data = data.filter(Q(year=year) | Q(parameter=parameter))
        

        serializer = SeasonalSerializer(data,many=True)

        return Response(serializer.data)
    

class AnnualView(APIView):
    def get(self,request):
        data = AnnualData.objects.all()

        year = request.GET.get('year')
        parameter = request.GET.get('parameter')
        region = request.GET.get('region')
        sort = request.GET.get('sort')

        data = get_annual_filtered_data(year,parameter,region,sort)

        serializer=AnnualSerializer(data,many=True)

        return Response(serializer.data)

    
