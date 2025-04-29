import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from api.models import Medication

@pytest.fixture
def user():
    """Создаем тестового пользователя."""
    user = get_user_model().objects.create_user(
        username='testuser',
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
def test_get_medications(api_client, user, medication):
    api_client.force_authenticate(user=user)  # аутентификация через токен
    response = api_client.get('/api/medications/')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['name'] == medication.name

@pytest.mark.django_db  # Разрешаем доступ к базе данных
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

@pytest.mark.django_db  # Разрешаем доступ к базе данных
def test_create_medication_invalid_data(api_client, user):
    api_client.force_authenticate(user=user)
    data = {
        'name': '',  # Некорректное имя
        'dosage': '500mg',
    }
    response = api_client.post('/api/medications/', data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'name' in response.data  # Ожидаем ошибку на поле name

@pytest.mark.django_db  # Разрешаем доступ к базе данных
def test_create_medication_without_name(api_client, user):
    api_client.force_authenticate(user=user)
    data = {
        'dosage': '500mg',
    }
    response = api_client.post('/api/medications/', data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'name' in response.data  # Ожидаем ошибку на поле name

@pytest.mark.django_db  # Разрешаем доступ к базе данных
def test_create_medication_without_dosage(api_client, user):
    api_client.force_authenticate(user=user)
    data = {
        'name': 'Aspirin',
    }
    response = api_client.post('/api/medications/', data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'dosage' in response.data  # Ожидаем ошибку на поле dosage

@pytest.mark.django_db  # Разрешаем доступ к базе данных
def test_update_medication(api_client, user, medication):
    api_client.force_authenticate(user=user)
    data = {
        'name': 'Ibuprofen Updated',
        'dosage': '400mg',
    }
    response = api_client.put(f'/api/medications/{medication.id}/', data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == 'Ibuprofen Updated'
    assert response.data['dosage'] == '400mg'

@pytest.mark.django_db  # Разрешаем доступ к базе данных
def test_delete_medication(api_client, user, medication):
    api_client.force_authenticate(user=user)
    response = api_client.delete(f'/api/medications/{medication.id}/')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    # Проверим, что лекарство действительно удалено
    assert not Medication.objects.filter(id=medication.id).exists()