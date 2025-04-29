from rest_framework import viewsets, permissions
from .models import Medication, MedicationSchedule, MedicationIntake, NotificationSettings
from .serializers import (
    MedicationSerializer,
    MedicationScheduleSerializer,
    MedicationIntakeSerializer,
    NotificationSettingsSerializer
)

class MedicationViewSet(viewsets.ModelViewSet):
    serializer_class = MedicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Medication.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class MedicationScheduleViewSet(viewsets.ModelViewSet):
    serializer_class = MedicationScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return MedicationSchedule.objects.filter(medication__user=self.request.user)

class MedicationIntakeViewSet(viewsets.ModelViewSet):
    serializer_class = MedicationIntakeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return MedicationIntake.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class NotificationSettingsViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSettingsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return NotificationSettings.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)