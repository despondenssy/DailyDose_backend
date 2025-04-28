from rest_framework import viewsets, permissions
from .models import Medication, Course
from .serializers import MedicationSerializer, CourseSerializer

# для обработки запросов с лекарствами
class MedicationViewSet(viewsets.ModelViewSet):
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Фильтруем лекарства по текущему пользователю
        return Medication.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # При создании лекарства автоматически присваиваем текущего пользователя
        serializer.save(user=self.request.user)

# для обработки курсов лечения
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Фильтруем курсы по текущему пользователю
        return Course.objects.filter(medication__user=self.request.user)

    def perform_create(self, serializer):
        # При создании курса автоматически присваиваем текущего пользователя
        serializer.save(user=self.request.user)