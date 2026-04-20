from django.urls import path, include
from .views import MonthlyViewSet, SeasonalViewSet, AnnualViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"monthly", MonthlyViewSet, basename="monthly")
router.register(r"seasonal", SeasonalViewSet, basename="seasonal")
router.register(r"annual", AnnualViewSet, basename="Annual")

urlpatterns = [
    path("", include(router.urls)),
]
