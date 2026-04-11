from django.urls import path
from .views import MonthlyView,SeasonalView,AnnualView,LoadData

urlpatterns=[
    path('loaddata/',LoadData.as_view()),
    path('monthly/',MonthlyView.as_view()),
    path('seasonal/',SeasonalView.as_view()),
    path('annual/',AnnualView.as_view()),
    path('monthly/<int:pk>/',MonthlyView.as_view()),
]