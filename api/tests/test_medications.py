import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from api.models import User, Medication
import re


@pytest.fixture
def user():
    return User.objects.create_user(id="user123", email="test@example.com", password="securepass", username="TestUser")


@pytest.fixture
def other_user():
    return User.objects.create_user(id="user999", email="other@example.com", password="password", username="OtherUser")


@pytest.fixture
def client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def medication_data():
    return {
        "id": "med1",
        "name": "Парацетамол",
        "form": "tablet",
        "dosagePerUnit": "500mg",  # camelCase
        "unit": "мг",
        "instructions": "После еды",
        "totalQuantity": 20,
        "remainingQuantity": 20,
        "lowStockThreshold": 5,
        "trackStock": True,
        "iconName": "pill",
        "iconColor": "blue",
        "createdAt": 1714825000000,
        "updatedAt": 1714825000000,
    }


def convert_camel_to_snake(data):
    """Преобразует ключи словаря из camelCase в snake_case."""
    def camel_to_snake(name):
        return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()

    return {camel_to_snake(k): v for k, v in data.items()}


@pytest.mark.django_db
def test_create_medication_success(client, medication_data):
    url = reverse("medication-list")
    response = client.post(url, medication_data, format="json")

    if response.status_code != 201:
        print(response.data)

    assert response.status_code == 201
    assert response.data["name"] == medication_data["name"]
    assert Medication.objects.filter(id="med1").exists()


@pytest.mark.django_db
def test_create_medication_missing_required_field(client, medication_data):
    medication_data.pop("name")
    url = reverse("medication-list")
    response = client.post(url, medication_data, format="json")

    assert response.status_code == 400
    assert "name" in response.data


@pytest.mark.django_db
def test_list_medications_only_user(client, user, other_user, medication_data):
    data_user = convert_camel_to_snake(medication_data)
    Medication.objects.create(**data_user, user=user)

    med2_data = medication_data.copy()
    med2_data["id"] = "med2"
    med2_data["name"] = "Ибупрофен"
    data_other = convert_camel_to_snake(med2_data)
    Medication.objects.create(**data_other, user=other_user)

    url = reverse("medication-list")
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["name"] == "Парацетамол"


@pytest.mark.django_db
def test_retrieve_medication(client, user, medication_data):
    data = convert_camel_to_snake(medication_data)
    med = Medication.objects.create(**data, user=user)
    url = reverse("medication-detail", kwargs={"pk": med.id})
    response = client.get(url)

    assert response.status_code == 200
    assert response.data["id"] == med.id


@pytest.mark.django_db
def test_update_medication(client, user, medication_data):
    data = convert_camel_to_snake(medication_data)
    med = Medication.objects.create(**data, user=user)
    url = reverse("medication-detail", kwargs={"pk": med.id})
    new_name = {"name": "Но-шпа"}
    response = client.patch(url, new_name, format="json")

    assert response.status_code == 200
    assert response.data["name"] == "Но-шпа"
    med.refresh_from_db()
    assert med.name == "Но-шпа"


@pytest.mark.django_db
def test_delete_medication(client, user, medication_data):
    data = convert_camel_to_snake(medication_data)
    med = Medication.objects.create(**data, user=user)
    url = reverse("medication-detail", kwargs={"pk": med.id})
    response = client.delete(url)

    assert response.status_code == 204
    assert not Medication.objects.filter(id=med.id).exists()


@pytest.mark.django_db
def test_user_cannot_access_other_medication(client, other_user, medication_data):
    data = convert_camel_to_snake(medication_data)
    med = Medication.objects.create(**data, user=other_user)
    url = reverse("medication-detail", kwargs={"pk": med.id})
    response = client.get(url)

    assert response.status_code == 404  # Нет доступа = будто не существует
