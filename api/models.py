from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class Medication(models.Model):
    class Form(models.TextChoices):
        TABLET = "tablet", "Таблетки"
        CAPSULE = "capsule", "Капсулы"
        DROPS = "drops", "Капли"
        LIQUID = "liquid", "Жидкость"
        OINTMENT = "ointment", "Мазь"
        SPRAY = "spray", "Спрей"
        POWDER = "powder", "Порошок"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='medications')
    name = models.CharField(max_length=100)
    form = models.CharField(max_length=20, choices=Form.choices)
    dosage_per_unit = models.CharField(max_length=100, blank=True, null=True)
    unit = models.CharField(max_length=50)
    instructions = models.TextField(blank=True, null=True)
    total_quantity = models.IntegerField(default=0)
    remaining_quantity = models.IntegerField(default=0)
    low_stock_threshold = models.IntegerField(default=0)
    track_stock = models.BooleanField(default=True)
    icon_name = models.CharField(max_length=50)
    icon_color = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class MedicationSchedule(models.Model):
    class Frequency(models.TextChoices):
        DAILY = "daily", "Ежедневно"
        EVERY_OTHER_DAY = "every_other_day", "Через день"
        SPECIFIC_DAYS = "specific_days", "Определённые дни недели"
        SPECIFIC_DATES = "specific_dates", "Определённые даты"

    class MealRelation(models.TextChoices):
        BEFORE_MEAL = "before_meal", "До еды"
        AFTER_MEAL = "after_meal", "После еды"
        WITH_MEAL = "with_meal", "Во время еды"
        NO_RELATION = "no_relation", "Не связано с едой"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='schedules')
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE, related_name='schedules')
    frequency = models.CharField(max_length=30, choices=Frequency.choices)
    days = models.JSONField(default=list)  # массив чисел 1-7 (понедельник–воскресенье)
    dates = models.JSONField(default=list)  # массив строк YYYY-MM-DD
    times = models.JSONField(default=list)  # массив объектов: { time: "HH:MM", dosage: "value", unit: "мг" }
    meal_relation = models.CharField(max_length=30, choices=MealRelation.choices)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    duration_days = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.medication.name} ({self.start_date})"


class MedicationIntake(models.Model):
    class Status(models.TextChoices):
        TAKEN = "taken", "Принято"
        MISSED = "missed", "Пропущено"
        PENDING = "pending", "Ожидается"

    schedule = models.ForeignKey(MedicationSchedule, on_delete=models.CASCADE, related_name='intakes')
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
    scheduled_time = models.TimeField()
    scheduled_date = models.DateField()
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    taken_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Дублируем поля для быстрого доступа
    medication_name = models.CharField(max_length=100)
    meal_relation = models.CharField(max_length=30, choices=MedicationSchedule.MealRelation.choices)
    dosage_per_unit = models.CharField(max_length=100, blank=True, null=True)
    instructions = models.TextField(blank=True, null=True)
    dosage_by_time = models.CharField(max_length=50)
    unit = models.CharField(max_length=50)
    icon_name = models.CharField(max_length=50)
    icon_color = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.medication_name} at {self.scheduled_time} on {self.scheduled_date}"


class NotificationSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notification_settings')
    medication_reminders_enabled = models.BooleanField(default=True)
    minutes_before_sheduled_time = models.IntegerField(default=15)
    low_stock_reminders_enabled = models.BooleanField(default=True)

    def __str__(self):
        return f"Notification settings for {self.user.email}"