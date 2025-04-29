import re
from rest_framework import serializers
from .models import User, Medication, MedicationSchedule, MedicationIntake, NotificationSettings


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = [
            'id', 'user', 'name', 'form', 'dosage_per_unit', 'unit', 'instructions',
            'total_quantity', 'remaining_quantity', 'low_stock_threshold', 'track_stock',
            'icon_name', 'icon_color', 'created_at', 'updated_at'
        ]
        read_only_fields = ('user', 'created_at', 'updated_at')

    def validate_dosage_per_unit(self, value):
        # Пример валидации дозировки (проверка, что значение соответствует формату)
        if not re.match(r'^\d+(mg|g|mcg)$', value):  # Ожидаем, что дозировка будет числом и единицей измерения (mg, g, mcg)
            raise serializers.ValidationError("Invalid dosage format. Expected format: number + unit (mg, g, mcg).")
        return value

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return Medication.objects.create(**validated_data)


class MedicationScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicationSchedule
        fields = [
            'id', 'user', 'medication', 'frequency', 'days', 'dates', 'times',
            'meal_relation', 'start_date', 'end_date', 'duration_days',
            'created_at', 'updated_at'
        ]
        read_only_fields = ('user', 'created_at', 'updated_at')

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return MedicationSchedule.objects.create(**validated_data)


class MedicationIntakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicationIntake
        fields = [
            'id', 'schedule', 'medication', 'scheduled_time', 'scheduled_date', 'status', 'taken_at',
            'created_at', 'medication_name', 'meal_relation', 'dosage_per_unit',
            'instructions', 'dosage_by_time', 'unit', 'icon_name', 'icon_color'
        ]
        read_only_fields = (
            'id', 'created_at',
            'medication', 'medication_name', 'meal_relation', 'dosage_per_unit',
            'instructions', 'unit', 'icon_name', 'icon_color'
        )

    def create(self, validated_data):
        schedule = validated_data['schedule']
        medication = schedule.medication

        # Автоматически проставляем связанные поля
        validated_data['medication'] = medication
        validated_data['medication_name'] = medication.name
        validated_data['meal_relation'] = schedule.meal_relation
        validated_data['dosage_per_unit'] = medication.dosage_per_unit
        validated_data['instructions'] = medication.instructions
        validated_data['unit'] = medication.unit
        validated_data['icon_name'] = medication.icon_name
        validated_data['icon_color'] = medication.icon_color

        return super().create(validated_data)


class NotificationSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationSettings
        fields = [
            'id', 'user', 'medication_reminders_enabled',
            'minutes_before_sheduled_time', 'low_stock_reminders_enabled'
        ]
        read_only_fields = ('user',)

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return NotificationSettings.objects.create(**validated_data)