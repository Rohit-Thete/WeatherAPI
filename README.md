"# WeatherAPI" 
# UK Climate Data REST API

A Django REST Framework API that serves historical UK climate data sourced from the UK Met Office. Supports monthly, seasonal, and annual weather observations across multiple UK regions and meteorological parameters.

---

## Tech Stack

- Python 3.x
- Django 4.x
- Django REST Framework
- SQLite (default) / PostgreSQL

---

## Project Structure

```
uk-climate-api/
├── manage.py
├── requirements.txt
├── README.md
└── api/
    ├── models.py          # Database models
    ├── serializers.py     # Read & write serializers
    ├── views.py           # ViewSets
    ├── urls.py            # Router configuration
    ├── constants.py       # Choices & parameter units
    └── utils.py           # Met Office data loader
```

---

## Setup

```bash
# 1. Clone the repo
git clone <repository-url>
cd uk-climate-api

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run migrations
python manage.py migrate

# 5. Start the server
python manage.py runserver
```

---

## Loading Data

Data is fetched from the Met Office public dataset using the `load_data()` utility:

```bash
python manage.py shell
>>> from api.utils import load_data
>>> load_data('England', 'Tmax')
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/monthly/` | List all monthly records |
| POST | `/monthly/` | Create a monthly record |
| GET | `/monthly/{id}/` | Retrieve a record |
| PUT/PATCH | `/monthly/{id}/` | Update a record |
| DELETE | `/monthly/{id}/` | Delete a record |
| GET | `/seasonal/` | List all seasonal records |
| POST | `/seasonal/` | Create a seasonal record |
| GET | `/seasonal/{id}/` | Retrieve a record |
| PUT/PATCH | `/seasonal/{id}/` | Update a record |
| DELETE | `/seasonal/{id}/` | Delete a record |
| GET | `/annual/` | List all annual records |
| POST | `/annual/` | Create an annual record |
| GET | `/annual/{id}/` | Retrieve a record |
| PUT/PATCH | `/annual/{id}/` | Update a record |
| DELETE | `/annual/{id}/` | Delete a record |

---

## Request & Response Examples

**POST /monthly/**
```json
{
  "year": 2023,
  "region": "England",
  "month": "january",
  "parameter": "Tmax",
  "value": 8.5
}
```

**Response (201 Created)**
```json
{
  "year": 2023,
  "region": "England",
  "month": "january",
  "value": 8.5,
  "parameter": "Tmax",
  "unit": "celsius"
}
```

---

## Supported Parameters

| Parameter | Unit |
|-----------|------|
| Tmax | celsius |
| Tmin | celsius |
| Tmean | celsius |
| Rainfall | mm |
| Sunshine | hours |
| Raindays1mm | days |
| AirFrost | days |
| Humidity | percent |
| WindSpeed | meters_per_second |
| Pressure | hPa |
| Snowfall | mm |

## Supported Regions

- UK
- England
- Scotland
- Wales
- Northern_Ireland
- England_and_Wales

---

## Validation

- `month` must be a lowercase month name e.g. `january`, `february`
- `season` must be one of: `winter`, `spring`, `summer`, `autumn`
- `parameter` must match exactly (case-sensitive) e.g. `Tmax` not `tmax`
- Invalid values return HTTP 400

---

## Models

All models inherit from the abstract `WeatherData` base which provides `year`, `region` (FK), `parameter` (FK), and `value`.

- **MonthlyData** — unique per (year, region, parameter, month)
- **SeasonalData** — unique per (year, region, parameter, season)
- **AnnualData** — unique per (year, region, parameter)
- **Region** — UK region name
- **Parameter** — meteorological parameter with associated unit
- **Unit** — unit of measurement

---

## Data Source

Climate data from the [UK Met Office](https://www.metoffice.gov.uk/pub/data/weather/uk/climate/datasets/) — used for educational purposes only.