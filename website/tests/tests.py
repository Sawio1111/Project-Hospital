import pytest

from website.models import Service, Qualification, Opinion
from django.contrib.auth.views import get_user_model
from medical_facility import settings


User = get_user_model()


@pytest.mark.django_db
def test_main_page(client, create_service, create_patient_opinion):
	response = client.get('/')
	assert response.status_code == 200
	assert len(response.context['services']) == 4
	assert len(response.context['opinions']) == 3


@pytest.mark.django_db
def test_login(client, create_patient_opinion):
	user = User.objects.first()
	response = client.post('/login/', {'username': user.username, 'password': user.password })
	assert response.status_code == 200


@pytest.mark.django_db
def test_registration(client, create_patient_opinion):
	users = User.objects.count()
	response = client.post('/registration/', {
		'password1': 'Szybkijakblyskawica12312312',
		'password2': 'Szybkijakblyskawica12312312',
		'last_name': 'Kubica',
		'first_name': 'Robert',
		'username': 'usernam90',
		'email': 'email@gmail.com',
		'pesel': 12345678911,
		'phone_number': 666777999,
		'contract': True,
		'sex': 1
	})
	assert users + 1 == User.objects.count()
	assert response.status_code == 302


@pytest.mark.django_db
def test_reset_password(client, create_patient_opinion):
	user = User.objects.first()
	response = client.post('/reset_password/', {
		'email': user.email
	})
	assert response.status_code == 302


@pytest.mark.django_db
def test_regulation_privacy(client):
	response = client.get('/about-us/privacy-policy-and-regulation/')
	assert response.status_code == 200


# @pytest.mark.django_db
# def test_logout(client, create_patient_opinion):
# 	user = User.objects.first()
# 	username = user.username
# 	password = user.password
# 	assert client.login(username=username, password=password)
# 	response = client.get('/account/profile/')
# 	assert response.status_code == 200