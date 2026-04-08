import requests
from .models import MonthlyData, SeasonalData, AnnualData, Region, Parameter,Unit,Year
from .constants import PARAMETER_UNITS,SEASONS,MONTHS




def load_data(region_name, parameter_name):
    unit_name = PARAMETER_UNITS.get(parameter_name)
    unit,_ = Unit.objects.get_or_create(name = unit_name) 

    region,_ = Region.objects.get_or_create(name = region_name)

    parameter,created =Parameter.objects.get_or_create(name = parameter_name,defaults={"unit":unit})

    if not created and parameter.unit != unit:
        parameter.unit = unit
        parameter.save()


    
    url = f"https://www.metoffice.gov.uk/pub/data/weather/uk/climate/datasets/{parameter_name}/date/{region_name}.txt"
    response = requests.get(url)
    lines = response.text.splitlines()

    for line in lines:
        col = line.split()

        # Skip invalid rows
        if len(col) < 17:
            continue
        if not col[0].isdigit():
            continue

        year_value = int(col[0])
        year,_ =Year.objects.get_or_create(year = year_value)




        # MONTHLY DATA
        for i in range(12):
            value = None if col[i + 1] == "---" else float(col[i + 1])
            if value is not None:
                MonthlyData.objects.get_or_create(
                    year=year,
                    region=region,
                    parameter=parameter,
                    month=MONTHS[i],
                    defaults={"value": value}
                )

        # SEASONAL DATA
        for i in range(4):
            value = None if col[13 + i] == "---" else float(col[13 + i])
            if value is not None:
                SeasonalData.objects.get_or_create(
                    year=year,
                    region=region,
                    parameter=parameter,
                    season=SEASONS[i],
                    defaults={"value": value}
                )

        # ANNUAL DATA
        annual_value = col[17]
        value = None if annual_value == "---" else float(annual_value)
        if value is  not None:
            AnnualData.objects.get_or_create(
                year=year,
                region=region,
                parameter=parameter,
                defaults={"value": value}
            )
        break

    print(f"Data loaded successfully for {region_name} - {parameter_name}")
    



# def get_monthly_filtered_data(year=None, parameter=None, region=None, month=None):
#     data = MonthlyData.objects.all()
#     if year:
#         data = data.filter(year=year)
#     if parameter:
#         data = data.filter(parameter__name=parameter)
#     if region:
#         data = data.filter(region__name=region)
#     if month:
#         data = data.filter(month=month)
#     return data


# def get_seasonal_filtered_data(year=None, parameter=None, region=None, season=None):
#     data = SeasonalData.objects.all()
#     if year:
#         data = data.filter(year=year)
#     if parameter:
#         data = data.filter(parameter__name=parameter)
#     if region:
#         data = data.filter(region__name=region)
#     if season:
#         data = data.filter(season=season)
#     return data


# def get_annual_filtered_data(year=None, parameter=None, region=None, sort=None):
#     data = AnnualData.objects.all()
#     if year:
#         data = data.filter(year=year)
#     if parameter:
#         data = data.filter(parameter__name=parameter)
#     if region:
#         data = data.filter(region__name=region)
#     if sort:
#         data = data.order_by(sort)
#     return data