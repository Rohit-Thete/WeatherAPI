from django.urls import path
from .views import MonthlyView,SeasonalView,AnnualView

urlpatterns=[
    path('monthly/',MonthlyView.as_view()),
    path('seasonal/',SeasonalView.as_view()),
    path('annual/',AnnualView.as_view()),
]