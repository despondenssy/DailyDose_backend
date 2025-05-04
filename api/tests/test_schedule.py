import pytest
import time
from datetime import date
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from api.models import Medication, MedicationSchedule, User
from api.serializers import MedicationScheduleSerializer


@pytest.fixture
def user(db):
    return User.objects.create_user(
        id="testuser123",
        email="test@example.com",
        password="testpass123",
        username="TestUser"
    )


@pytest.fixture
def auth_client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def medication(user):
    return Medication.objects.create(
        id="med123",
        user=user,
        name="TestMed",
        form="tablet",
        dosage_per_unit="10mg",
        unit="mg",
        instructions="Take after meal",
        total_quantity=30,
        remaining_quantity=20,
        low_stock_threshold=5,
        track_stock=True,
        icon_name="pill",
        icon_color="blue",
        created_at=int(time.time() * 1000),
        updated_at=int(time.time() * 1000)
    )


@pytest.fixture
def schedule(medication):
    return MedicationSchedule.objects.create(
        id="sched123",
        user=medication.user,
        medication=medication,
        frequency="daily",
        days=[1, 2],
        dates=[],
        times=[{"time": "09:00", "dosage": "1", "unit": "mg"}],
        meal_relation="no_relation",
        start_date=date.today(),
        duration_days=3,
        created_at=int(time.time() * 1000),
        updated_at=int(time.time() * 1000)
    )


@pytest.mark.django_db
def test_create_schedule(auth_client, medication):
    url = reverse("schedule-list")
    payload = {
        "id": "new_sched123",
        "medicationId": medication.id,
        "frequency": "daily",
        "days": [1, 2, 3],
        "dates": [],
        "times": [{"time": "08:00", "dosage": "1", "unit": "mg"}],
        "mealRelation": "after_meal",
        "startDate": str(date.today()),
        "endDate": None,
        "durationDays": 7,
        "createdAt": int(time.time() * 1000),
        "updatedAt": int(time.time() * 1000)
    }

    response = auth_client.post(url, payload, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert MedicationSchedule.objects.filter(id="new_sched123").exists()


@pytest.mark.django_db
def test_create_schedule_invalid_medication(auth_client, user):
    url = reverse("schedule-list")
    payload = {
        "id": "invalid_sched",
        "medicationId": "non_existing",
        "frequency": "daily",
        "days": [],
        "dates": [],
        "times": [{"time": "08:00", "dosage": "1", "unit": "mg"}],
        "mealRelation": "before_meal",
        "startDate": str(date.today()),
        "durationDays": 3,
        "endDate": None,
        "createdAt": int(time.time() * 1000),
        "updatedAt": int(time.time() * 1000)
    }

    response = auth_client.post(url, payload, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "medication" in response.data


@pytest.mark.django_db
def test_update_schedule(auth_client, schedule):
    url = reverse("schedule-detail", args=[schedule.id])
    update_data = {
        "id": schedule.id,
        "medicationId": schedule.medication.id,
        "frequency": "specific_days",
        "days": [1, 3, 5],
        "dates": [],
        "times": [{"time": "10:00", "dosage": "2", "unit": "mg"}],
        "mealRelation": "with_meal",
        "startDate": str(date.today()),
        "endDate": None,
        "durationDays": 5,
        "createdAt": schedule.created_at,
        "updatedAt": int(time.time() * 1000)
    }

    response = auth_client.put(url, update_data, format="json")
    assert response.status_code == status.HTTP_200_OK
    schedule.refresh_from_db()
    assert schedule.frequency == "specific_days"


@pytest.mark.django_db
def test_schedule_missing_required_fields(auth_client, medication):
    url = reverse("schedule-list")
    invalid_data = {
        "id": "missing_fields",
        "medicationId": medication.id,
        "startDate": str(date.today())
    }

    response = auth_client.post(url, invalid_data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    # Проверяем только основные обязательные поля
    assert "frequency" in response.data
    assert "mealRelation" in response.data


@pytest.mark.django_db
def test_schedule_end_date_optional(auth_client, medication):
    url = reverse("schedule-list")
    payload = {
        "id": "optional_end_date",
        "medicationId": medication.id,
        "frequency": "daily",
        "days": [],
        "dates": [],
        "times": [{"time": "07:00", "dosage": "1", "unit": "mg"}],
        "mealRelation": "before_meal",
        "startDate": str(date.today()),
        "durationDays": 10,
        "endDate": None,
        "createdAt": int(time.time() * 1000),
        "updatedAt": int(time.time() * 1000)
    }

    response = auth_client.post(url, payload, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["endDate"] is None


@pytest.mark.django_db
def test_serializer_valid_schedule(medication, user):
    payload = {
        "id": "serial_valid",
        "userId": user.id,
        "medicationId": medication.id,
        "frequency": "daily",
        "days": [],
        "dates": [],
        "times": [{"time": "10:00", "dosage": "1", "unit": "mg"}],
        "mealRelation": "no_relation",
        "startDate": str(date.today()),
        "durationDays": 5,
        "endDate": None,
        "createdAt": int(time.time() * 1000),
        "updatedAt": int(time.time() * 1000)
    }

    serializer = MedicationScheduleSerializer(data=payload)
    assert serializer.is_valid(), serializer.errors


@pytest.mark.django_db
def test_serializer_missing_times(medication, user):
    payload = {
        "id": "serial_no_times",
        "userId": user.id,
        "medicationId": medication.id,
        "frequency": "daily",
        "days": [],
        "dates": [],
        "times": [],  # Пустой массив times
        "mealRelation": "no_relation",
        "startDate": str(date.today()),
        "durationDays": 5,
        "endDate": None,
        "createdAt": int(time.time() * 1000),
        "updatedAt": int(time.time() * 1000)
    }

    serializer = MedicationScheduleSerializer(data=payload)
    assert not serializer.is_valid()
    assert "times" in serializer.errors