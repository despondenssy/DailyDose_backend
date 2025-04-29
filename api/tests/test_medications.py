import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from api.models import Medication

@pytest.fixture
def user():
    """Создаем тестового пользователя."""
    user = get_user_model().objects.create_user(
        username='testuser',  # Добавлено обязательное поле username
        email='testuser@example.com',
        password='testpassword123'
    )
    return user

@pytest.fixture
def api_client():
    """Создаем экземпляр клиента для API."""
    return APIClient()

@pytest.fixture
def medication(user):
    """Создаем тестовое лекарство для пользователя."""
    medication = Medication.objects.create(
        user=user,
        name="Ibuprofen",
        dosage="200mg"
    )
    return medication

@pytest.mark.django_db  # Разрешаем доступ к базе данных
# Тестируем эндпоинт для получения всех лекарств
def test_get_medications(api_client, user, medication):
    api_client.force_authenticate(user=user)  # аутентификация через токен
    response = api_client.get('/api/medications/')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['name'] == medication.name

@pytest.mark.django_db  # Разрешаем доступ к базе данных
# Тестируем создание нового лекарства
def test_create_medication(api_client, user):
    api_client.force_authenticate(user=user)
    data = {
        'name': 'Paracetamol',
        'dosage': '500mg',
    }
    response = api_client.post('/api/medications/', data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['name'] == 'Paracetamol'
    assert response.data['dosage'] == '500mg'