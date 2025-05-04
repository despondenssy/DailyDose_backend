import pytest
import time
from datetime import date
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from api.models import Medication, MedicationSchedule, MedicationIntake, User
from api.serializers import MedicationIntakeSerializer


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


@pytest.fixture
def intake(schedule):
    return MedicationIntake.objects.create(
        id="intake123",
        schedule=schedule,
        medication=schedule.medication,
        user=schedule.user,
        scheduled_time="09:00",
        scheduled_date=str(date.today()),
        status="pending",
        medication_name=schedule.medication.name,
        meal_relation=schedule.meal_relation,
        dosage_per_unit=schedule.medication.dosage_per_unit,
        instructions=schedule.medication.instructions,
        dosage_by_time="1",
        unit="mg",
        icon_name=schedule.medication.icon_name,
        icon_color=schedule.medication.icon_color,
        created_at=int(time.time() * 1000),
        updated_at=int(time.time() * 1000)
    )


@pytest.mark.django_db
def test_create_intake(auth_client, schedule):
    url = reverse("intake-list")
    payload = {
        "id": "new_intake123",
        "scheduleId": schedule.id,
        "medicationId": schedule.medication.id,
        "scheduledTime": "10:00",
        "scheduledDate": str(date.today()),
        "status": "pending",
        "medicationName": schedule.medication.name,
        "mealRelation": schedule.meal_relation,
        "dosagePerUnit": schedule.medication.dosage_per_unit,
        "dosageByTime": "1",
        "unit": "mg",
        "instructions": schedule.medication.instructions,
        "iconName": schedule.medication.icon_name,
        "iconColor": schedule.medication.icon_color,
        "createdAt": int(time.time() * 1000),
        "updatedAt": int(time.time() * 1000)
    }

    response = auth_client.post(url, payload, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert MedicationIntake.objects.filter(id="new_intake123").exists()


@pytest.mark.django_db
def test_create_intake_invalid_schedule(auth_client, medication):
    url = reverse("intake-list")
    payload = {
        "id": "invalid_intake",
        "scheduleId": "non_existing",
        "medicationId": medication.id,
        "scheduledTime": "10:00",
        "scheduledDate": str(date.today()),
        "status": "pending",
        "medicationName": medication.name,
        "mealRelation": "no_relation",
        "dosagePerUnit": medication.dosage_per_unit,
        "dosageByTime": "1",
        "unit": "mg",
        "instructions": medication.instructions,
        "iconName": medication.icon_name,
        "iconColor": medication.icon_color,
        "createdAt": int(time.time() * 1000),
        "updatedAt": int(time.time() * 1000)
    }

    response = auth_client.post(url, payload, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    # Проверяем текст ошибки, так как она возвращается как список
    assert "Расписание с таким ID не найдено" in str(response.data)


@pytest.mark.django_db
def test_update_intake_status(auth_client, intake):
    url = reverse("intake-detail", args=[intake.id])
    update_data = {
        "status": "taken",
        "takenAt": int(time.time() * 1000),
        "updatedAt": int(time.time() * 1000)
    }

    response = auth_client.patch(url, update_data, format="json")
    assert response.status_code == status.HTTP_200_OK
    intake.refresh_from_db()
    assert intake.status == "taken"
    assert intake.taken_at is not None


@pytest.mark.django_db
def test_intake_missing_required_fields(auth_client, schedule):
    url = reverse("intake-list")
    invalid_data = {
        "id": "missing_fields",
        "scheduleId": schedule.id,
        "medicationId": schedule.medication.id,
        "medicationName": schedule.medication.name,
        "mealRelation": schedule.meal_relation,
        "dosagePerUnit": schedule.medication.dosage_per_unit,
        "instructions": schedule.medication.instructions,
        "dosageByTime": "1",
        "unit": "mg",
        "iconName": schedule.medication.icon_name,
        "iconColor": schedule.medication.icon_color,
        "createdAt": int(time.time() * 1000),
        "updatedAt": int(time.time() * 1000)
    }

    response = auth_client.post(url, invalid_data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    # Проверяем только действительно обязательные поля
    required_fields = {"scheduledTime", "scheduledDate"}
    assert all(field in response.data for field in required_fields)


@pytest.mark.django_db
def test_serializer_valid_intake(schedule):
    payload = {
        "id": "serial_valid",
        "scheduleId": schedule.id,
        "medicationId": schedule.medication.id,
        "scheduledTime": "10:00",
        "scheduledDate": str(date.today()),
        "status": "pending",
        "medicationName": schedule.medication.name,
        "mealRelation": schedule.meal_relation,
        "dosagePerUnit": schedule.medication.dosage_per_unit,
        "dosageByTime": "1",
        "unit": "mg",
        "instructions": schedule.medication.instructions,
        "iconName": schedule.medication.icon_name,
        "iconColor": schedule.medication.icon_color,
        "createdAt": int(time.time() * 1000),
        "updatedAt": int(time.time() * 1000)
    }

    serializer = MedicationIntakeSerializer(data=payload)
    assert serializer.is_valid(), serializer.errors


@pytest.mark.django_db
def test_get_intakes_for_schedule(auth_client, schedule, intake):
    url = reverse("intake-list")
    response = auth_client.get(url, {"scheduleId": schedule.id}, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["id"] == intake.id