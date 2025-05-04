import pytest
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIRequestFactory

from api.serializers import UserSerializer, UserCreateSerializer

User = get_user_model()

@pytest.mark.django_db
def test_user_str_representation():
    user = User.objects.create_user(id="user123", username="liza", email="test@example.com", password="testpass123")
    assert str(user) == "test@example.com"

@pytest.mark.django_db
def test_user_serializer_output():
    user = User.objects.create_user(id="user456", username="liza", email="liza@example.com", password="test1234")
    serializer = UserSerializer(user)
    assert serializer.data["id"] == "user456"
    assert serializer.data["name"] == "liza"
    assert serializer.data["email"] == "liza@example.com"

@pytest.mark.django_db
def test_user_create_serializer_valid_data():
    data = {
        "id": "abc123",
        "name": "newuser",
        "email": "newuser@example.com",
        "password": "supersecurepass"
    }
    factory = APIRequestFactory()
    request = factory.post("/users/")
    serializer = UserCreateSerializer(data=data, context={"request": request})
    assert serializer.is_valid(), serializer.errors
    user = serializer.save()
    assert user.username == "newuser"
    assert user.email == "newuser@example.com"
    assert user.id == "abc123"
    assert user.check_password("supersecurepass")

@pytest.mark.django_db
def test_user_create_serializer_missing_fields():
    data = {
        "email": "missing@example.com",
        "password": "pass1234"
        # Нет поля 'id' и 'name'
    }
    factory = APIRequestFactory()
    request = factory.post("/users/")
    serializer = UserCreateSerializer(data=data, context={"request": request})
    assert not serializer.is_valid()
    assert "id" in serializer.errors
    assert "name" in serializer.errors