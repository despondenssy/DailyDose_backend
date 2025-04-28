from rest_framework import serializers
from .models import User, Medication, Course

# Сериализатор для пользователя
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')  # Только те поля, которые нужны

# Сериализатор для лекарства
class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = ('id', 'name', 'dosage', 'icon')  # 'user' будет автоматически привязан

    def create(self, validated_data):
        # Привязываем пользователя к создаваемому объекту лекарства
        user = self.context['request'].user  # Получаем пользователя из контекста запроса
        validated_data['user'] = user  # Добавляем пользователя в validated_data
        return Medication.objects.create(**validated_data)  # Создаем объект без передачи 'user' явно

# Сериализатор для курса лечения    
class CourseSerializer(serializers.ModelSerializer):
    medication_name = serializers.CharField(source='medication.name', read_only=True)

    class Meta:
        model = Course
        fields = ('id', 'medication', 'medication_name', 'start_date', 'end_date', 'frequency', 'meal_relation', 'times_per_day')

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)