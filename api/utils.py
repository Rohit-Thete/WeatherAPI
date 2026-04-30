import requests
from .models import MonthlyData, SeasonalData, AnnualData, Region, Parameter, Unit
from .constants import PARAMETER_UNITS, SEASONS, MONTHS


def load_data(region_name, parameter_name):
    unit_name = PARAMETER_UNITS.get(parameter_name)
    unit, _ = Unit.objects.get_or_create(name=unit_name)

    region, _ = Region.objects.get_or_create(name=region_name)

    parameter, created = Parameter.objects.get_or_create(
        name=parameter_name, defaults={"unit": unit}
    )

    if not created and parameter.unit != unit:
        parameter.unit = unit
        parameter.save()

    url = f"https://www.metoffice.gov.uk/pub/data/weather/uk/climate/datasets/{parameter_name}/date/{region_name}.txt"
    response = requests.get(url)
    lines = response.text.splitlines()

    # 🔹 batches
    monthly_batch = []
    seasonal_batch = []
    annual_batch = []

    batch_size = 1000

    # 🔹 preload existing (for resume)
    existing_monthly = set(
        MonthlyData.objects.filter(region=region, parameter=parameter)
        .values_list("year", "month")
    )

    for line in lines:
        col = line.split()

        if len(col) < 17:
            continue
        if not col[0].isdigit():
            continue

        year = int(col[0])

        # 🔥 MONTHLY
        for i in range(12):
            value = None if col[i + 1] == "---" else float(col[i + 1])

            if value is None:
                continue

            key = (year, MONTHS[i])

            if key in existing_monthly:
                continue

            monthly_batch.append(
                MonthlyData(
                    year=year,
                    region=region,
                    parameter=parameter,
                    month=MONTHS[i],
                    value=value,
                )
            )

            existing_monthly.add(key)

        # 🔥 SEASONAL
        for i in range(4):
            value = None if col[13 + i] == "---" else float(col[13 + i])

            if value is None:
                continue

            seasonal_batch.append(
                SeasonalData(
                    year=year,
                    region=region,
                    parameter=parameter,
                    season=SEASONS[i],
                    value=value,
                )
            )

        # 🔥 ANNUAL
        annual_value = col[17]
        value = None if annual_value == "---" else float(annual_value)

        if value is not None:
            annual_batch.append(
                AnnualData(
                    year=year,
                    region=region,
                    parameter=parameter,
                    value=value,
                )
            )

        # 🔹 BULK INSERT (monthly)
        if len(monthly_batch) >= batch_size:
            MonthlyData.objects.bulk_create(monthly_batch, ignore_conflicts=True)
            monthly_batch.clear()

        # 🔹 BULK INSERT (seasonal)
        if len(seasonal_batch) >= batch_size:
            SeasonalData.objects.bulk_create(seasonal_batch, ignore_conflicts=True)
            seasonal_batch.clear()

        # 🔹 BULK INSERT (annual)
        if len(annual_batch) >= batch_size:
            AnnualData.objects.bulk_create(annual_batch, ignore_conflicts=True)
            annual_batch.clear()

    # 🔹 FINAL INSERT
    if monthly_batch:
        MonthlyData.objects.bulk_create(monthly_batch, ignore_conflicts=True)

    if seasonal_batch:
        SeasonalData.objects.bulk_create(seasonal_batch, ignore_conflicts=True)

    if annual_batch:
        AnnualData.objects.bulk_create(annual_batch, ignore_conflicts=True)

    print(f"✅ Data loaded successfully for {region_name} - {parameter_name}")


def get_parameter_obj(parameter_name):
    unit_name = PARAMETER_UNITS.get(parameter_name)
    unit_obj, _ = Unit.objects.get_or_create(name=unit_name)
    parameter_obj, created = Parameter.objects.get_or_create(
        name=parameter_name, defaults={"unit": unit_obj}
    )

    if not created and parameter_obj.unit != unit_obj:
        parameter_obj.unit = unit_obj
        parameter_obj.save()

    return parameter_obj


def load_parameters():
    from .models import Parameter, Unit
    from .constants import PARAMETER_CHOICES, PARAMETER_UNITS

    for name, _ in PARAMETER_CHOICES:
        unit_name = PARAMETER_UNITS.get(name)
        unit_obj, _ = Unit.objects.get_or_create(name=unit_name)

        Parameter.objects.get_or_create(name=name, defaults={"unit": unit_obj})


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
