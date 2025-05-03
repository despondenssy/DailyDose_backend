from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter #тк viewset реализует сразу несколько операций используем router
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
    path('', include(router.urls)), #все адреса с роутера будут доступны здесь
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#последнее для обработки фото