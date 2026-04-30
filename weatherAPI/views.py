from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import TemplateView

from api.constants import MONTH_CHOICES, PARAMETER_CHOICES, SEASON_CHOICES
from api.models import AnnualData, MonthlyData, Region, SeasonalData


@method_decorator(ensure_csrf_cookie, name="dispatch")
class HomeView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["stats"] = {
            "monthly": MonthlyData.objects.count(),
            "seasonal": SeasonalData.objects.count(),
            "annual": AnnualData.objects.count(),
            "regions": Region.objects.count(),
        }
        context["parameter_choices"] = [value for value, _ in PARAMETER_CHOICES]
        context["month_choices"] = [value for value, _ in MONTH_CHOICES]
        context["season_choices"] = [value for value, _ in SEASON_CHOICES]
        context["region_suggestions"] = list(
            Region.objects.order_by("name").values_list("name", flat=True)
        )
        context["app_config"] = {
            "pageSize": settings.REST_FRAMEWORK.get("PAGE_SIZE", 10),
            "datasets": {
                "monthly": {
                    "label": "Monthly",
                    "endpoint": "/monthly/",
                    "periodField": "month",
                    "periodLabel": "Month",
                    "columns": [
                        {"key": "year", "label": "Year"},
                        {"key": "region", "label": "Region"},
                        {"key": "month", "label": "Month"},
                        {"key": "parameter", "label": "Parameter"},
                        {"key": "value", "label": "Value"},
                        {"key": "unit", "label": "Unit"},
                    ],
                },
                "seasonal": {
                    "label": "Seasonal",
                    "endpoint": "/seasonal/",
                    "periodField": "season",
                    "periodLabel": "Season",
                    "columns": [
                        {"key": "year", "label": "Year"},
                        {"key": "region", "label": "Region"},
                        {"key": "season", "label": "Season"},
                        {"key": "parameter", "label": "Parameter"},
                        {"key": "value", "label": "Value"},
                        {"key": "unit", "label": "Unit"},
                    ],
                },
                "annual": {
                    "label": "Annual",
                    "endpoint": "/annual/",
                    "periodField": None,
                    "periodLabel": None,
                    "columns": [
                        {"key": "year", "label": "Year"},
                        {"key": "region", "label": "Region"},
                        {"key": "parameter", "label": "Parameter"},
                        {"key": "value", "label": "Value"},
                        {"key": "unit", "label": "Unit"},
                    ],
                },
            },
        }
        return context
