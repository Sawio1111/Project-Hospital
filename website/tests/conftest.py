import pytest

from django.test import Client
from .utils import faker
from website.models import Service, Qualification, Opinion
from website.views import User


@pytest.fixture
def client():
	client = Client()
	return client


@pytest.fixture
def create_service():
	for i in range(8):
		Service.objects.create(
			name=faker.name(),
			description=faker.sentence()
		)


@pytest.fixture
def create_patient_opinion():
	for i in range(10):
		user = User.objects.create(
			last_name=faker.last_name(),
			first_name=faker.first_name(),
			username=faker.name(),
			email=faker.email(),
			pesel=faker.pesel(),
			sex=1,
			phone_number=faker.random_int(0, 9),
			status=1,
		)
		user.set_password(faker.password())
		user.save()
		Opinion.objects.create(
			rating=faker.random_int(1, 10),
			description=faker.sentence(),
			status=2,
			author=user
		)


@pytest.fixture
def create_doctor_service_qualification():
	for i in range(8):
		Service.objects.create(
			name=faker.name(),
			description=faker.sentence()
		)

	for i in range(10):
		doctor = User.objects.create(
			last_name=faker.last_name(),
			first_name=faker.first_name(),
			username=faker.name(),
			email=faker.email(),
			pesel=faker.pesel(),
			sex=faker.random_int(1, 2),
			phone_number=faker.phone_number(),
			status=2,
		)
		doctor.set_password(faker.password())
		doctor.save()
		Qualification.objects.create(
			salary=faker.random_int(1000, 2000),
			price=faker.random_int(20, 100),
			degree=faker.name(),
			doctor=doctor,
			room=faker.random_int(1, 100),
			service_id=faker.random_int(1, 8)
		)
