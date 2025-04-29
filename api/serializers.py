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
        read_only_fields = ('created_at',)


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