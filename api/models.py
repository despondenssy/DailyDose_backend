from django.db import models
from django.contrib.auth.models import AbstractUser

# Кастомный пользователь
class User(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

# Лекарство
class Medication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='medications')
    name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=100)
    icon = models.CharField(max_length=100, blank=True, null=True)  # вдруг в приложении можно выбрать иконку

    def __str__(self):
        return self.name

# Курс приема лекарства
class Course(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')  # Добавляем связь с пользователем
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE, related_name='courses')
    start_date = models.DateField()
    end_date = models.DateField()
    frequency = models.CharField(max_length=100)
    meal_relation = models.CharField(max_length=100, blank=True, null=True)
    times_per_day = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.medication.name} ({self.start_date} - {self.end_date})"