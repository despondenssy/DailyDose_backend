from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MedicationViewSet,
    MedicationScheduleViewSet,
    MedicationIntakeViewSet,
    NotificationSettingsViewSet
)

router = DefaultRouter()
router.register(r'medications', MedicationViewSet, basename='medication')
router.register(r'schedules', MedicationScheduleViewSet, basename='schedule')
router.register(r'intakes', MedicationIntakeViewSet, basename='intake')
router.register(r'notifications', NotificationSettingsViewSet, basename='notification')

urlpatterns = [
    path('', include(router.urls)),
]