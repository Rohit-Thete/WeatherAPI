import requests
from .models import MonthlyData, SeasonalData, AnnualData


def load_data(region, parameter):
    region=region.strip()

    url = f"https://www.metoffice.gov.uk/pub/data/weather/uk/climate/datasets/{parameter}/date/{region}.txt"

    response = requests.get(url)
    lines = response.text.splitlines()

    months = ["Jan","Feb","Mar","Apr","May","Jun",
              "Jul","Aug","Sep","Oct","Nov","Dec"]

    seasons = ["Win","Spr","Sum","Aut","Ann"]

    for line in lines:

        col = line.split()

        # skip invalid rows
        if len(col) < 13:
            continue

        if not col[0].isdigit():
            continue

        year = int(col[0])

        # -------- MONTH DATA --------
        for i in range(12):
            value = col[i+1]

            if value == "---":
                temp = None
            else:
                temp = float(value)


            MonthlyData.objects.create(
                year=year,
                region=region,
                parameter=parameter,
                month=months[i].strip(),
                temprature=temp
            )

        # -------- SEASON DATA --------
        for i in range(5):
            value = col[13+i]

            if value == "---":
                temp = None
            else:
                temp = float(value)

            SeasonalData.objects.create(
                year=year,
                region=region,
                parameter=parameter,
                season=seasons[i].strip(),
                temprature=temp
            )

        # -------- ANNUAL DATA --------
        for i in range(1):
            annual_value = col[17+i]

            if annual_value == "---":
                temp = None
            else:
                temp = float(annual_value)

                print("ANNUAL:", temp)

            AnnualData.objects.create(
            year=year,
            region=region,
            parameter=parameter,
            temprature=temp
            )

    print("Data stored successfully")



# def get_monthly_filtered_data(year=None,parameter=None,region=None,month=None):
        
#     data = MonthlyData.objects.all()
#     if year:
#         data = data.filter(year=year)

#     if parameter:
#         data = data.filter(parameter=parameter)

#     if region:
#         data = data.filter(region=region)
        
#     if month:
#         data = data.filter(month=month)

#         return data


# def get_seasonal_filtered_data(year=None,parameter=None,region=None,season=None):
   
    
# def get_annual_filtered_data(year=None,parameter=None,region=None,sort=None):

    