import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from api.models import Medication


@pytest.fixture
def user():
    return get_user_model().objects.create_user(
        username='testuser',
        email='testuser@example.com',
        password='testpassword123'
    )


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def medication(user):
    return Medication.objects.create(
        user=user,
        name="Ibuprofen",
        form="tablet",
        dosage_per_unit="200mg",
        unit="mg",
        instructions="Take one tablet every 4-6 hours",
        total_quantity=30,
        remaining_quantity=30,
        low_stock_threshold=5,
        track_stock=True,
        icon_name="pill",
        icon_color="blue"
    )


@pytest.mark.django_db
def test_get_medications(api_client, user, medication):
    api_client.force_authenticate(user=user)
    response = api_client.get('/api/medications/')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['name'] == medication.name


@pytest.mark.django_db
def test_create_medication(api_client, user):
    api_client.force_authenticate(user=user)
    data = {
        'name': 'Paracetamol',
        'form': 'tablet',
        'dosage_per_unit': '500mg',
        'unit': 'mg',
        'instructions': 'Take one tablet every 4 hours',
        'total_quantity': 100,
        'remaining_quantity': 100,
        'low_stock_threshold': 10,
        'track_stock': True,
        'icon_name': 'pill',
        'icon_color': 'green'
    }
    response = api_client.post('/api/medications/', data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['name'] == 'Paracetamol'
    assert response.data['dosage_per_unit'] == '500mg'
    assert response.data['total_quantity'] == 100
    assert response.data['remaining_quantity'] == 100


@pytest.mark.django_db
def test_create_medication_invalid_data(api_client, user):
    api_client.force_authenticate(user=user)
    data = {
        'name': '',
        'form': 'capsule',
        'dosage_per_unit': '250mg',
        'unit': 'mg',
        'icon_name': 'pill',
        'icon_color': 'red'
    }
    response = api_client.post('/api/medications/', data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'name' in response.data


@pytest.mark.django_db
def test_create_medication_missing_required_field(api_client, user):
    api_client.force_authenticate(user=user)
    data = {
        'name': 'Aspirin',
        'form': 'tablet',
        # Пропущен unit
        'dosage_per_unit': '100mg',
        'icon_name': 'pill',
        'icon_color': 'red'
    }
    response = api_client.post('/api/medications/', data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'unit' in response.data


@pytest.mark.django_db
def test_update_medication(api_client, user, medication):
    api_client.force_authenticate(user=user)
    data = {
        'name': 'Ibuprofen Updated',
        'form': 'tablet',
        'dosage_per_unit': '400mg',
        'unit': 'mg',
        'instructions': 'Take two tablets every 4-6 hours',
        'total_quantity': 50,
        'remaining_quantity': 50,
        'low_stock_threshold': 10,
        'track_stock': True,
        'icon_name': 'pill',
        'icon_color': 'blue'
    }
    response = api_client.put(f'/api/medications/{medication.id}/', data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == 'Ibuprofen Updated'
    assert response.data['dosage_per_unit'] == '400mg'


@pytest.mark.django_db
def test_delete_medication(api_client, user, medication):
    api_client.force_authenticate(user=user)
    response = api_client.delete(f'/api/medications/{medication.id}/')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Medication.objects.filter(id=medication.id).exists()