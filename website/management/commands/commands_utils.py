import datetime
import random
import faker

from website.models import Service, Qualification, Appointment, Opinion, DateTimeWork, AppointmentNotes, TimeAppointment
from django.contrib.auth.models import Permission
from django.contrib.auth.views import get_user_model
from django.utils import timezone

faker = faker.Faker("pl-PL")

User = get_user_model()


def create_service(name):
	return Service.objects.create(
		name=name,
		description=faker.sentence()
	)


def create_patient():
	patient = User.objects.create(
		last_name=faker.last_name(),
		first_name=faker.first_name(),
		username=faker.name(),
		email=faker.email(),
		pesel=faker.pesel(),
		sex=1,
		phone_number=faker.random_int(0, 9),
		status=1
	)
	patient.set_password(faker.password())
	patient.save()
	permission = Permission.objects.get(codename='client_permission')
	patient.user_permissions.add(permission)
	return patient


def create_doctor():
	doctor = User.objects.create(
		last_name=faker.last_name(),
		first_name=faker.first_name(),
		username=faker.name(),
		email=faker.email(),
		pesel=faker.pesel(),
		sex=1,
		phone_number=faker.random_int(0, 9),
		status=2
	)
	doctor.set_password(faker.password())
	doctor.save()
	permission = Permission.objects.get(codename='doctor_permission')
	doctor.user_permissions.add(permission)
	return doctor


def create_admin_test(username='admin', password='admin'):
	admin = User.objects.create(
		last_name=faker.last_name(),
		first_name=faker.first_name(),
		username=username,
		email=faker.email(),
		pesel=faker.pesel(),
		sex=1,
		phone_number=faker.random_int(0, 9),
		status=3
	)
	admin.set_password(password)
	admin.save()
	permission = Permission.objects.get(codename='administrator_permission')
	admin.user_permissions.add(permission)
	return admin


def create_doctor_test(username='doctor', password='doctor'):
	doctor = User.objects.create(
		last_name=faker.last_name(),
		first_name=faker.first_name(),
		username=username,
		email=faker.email(),
		pesel=faker.pesel(),
		sex=1,
		phone_number=faker.random_int(0, 9),
		status=2
	)
	doctor.set_password(password)
	doctor.save()
	permission = Permission.objects.get(codename='doctor_permission')
	doctor.user_permissions.add(permission)
	return doctor


def create_patient_test(username='patient', password='patient'):
	patient = User.objects.create(
		last_name=faker.last_name(),
		first_name=faker.first_name(),
		username=username,
		email=faker.email(),
		pesel=faker.pesel(),
		sex=1,
		phone_number=faker.random_int(0, 9),
		status=1
	)
	patient.set_password(password)
	patient.save()
	permission = Permission.objects.get(codename='client_permission')
	patient.user_permissions.add(permission)
	return patient


def create_opinion(user):
	return Opinion.objects.create(
		rating=faker.random_int(1, 10),
		description=faker.sentence(),
		status=2,
		author=user
	)


def create_qualification(doctor, service):
	return 	Qualification.objects.create(
			salary=faker.random_int(1000, 2000),
			price=faker.random_int(20, 100),
			degree=faker.name(),
			doctor=doctor,
			room=faker.random_int(1, 100),
			service=service
		)


def create_datetimework(doctor):
	date = DateTimeWork.objects.create(
		date_from=timezone.localtime(timezone.now()).date(),
		date_to=timezone.localtime(timezone.now() + timezone.timedelta(days=random.randint(1, 30))).date(),
		time_from=datetime.time(8, 0, 0),
		time_to=datetime.time(16, 0, 0),
		status=random.randint(1, 2),
		visit_time=random.randint(10, 30),
		doctor=doctor
	)
	time_from = datetime.datetime.combine(datetime.datetime.today(), date.time_from)
	time_to = datetime.datetime.combine(datetime.datetime.today(), date.time_to)
	new_time = time_from
	while new_time <= time_to:
		if '13' not in new_time.strftime('%H:%M'):
			TimeAppointment.objects.create(
				date_time_work=date,
				visit_time=new_time
			)
		new_time = new_time + datetime.timedelta(minutes=date.visit_time)
	return date




def create_appointment(patient, doctor, date, time):
	return Appointment.objects.create(
		patient=patient,
		doctor=doctor,
		date=date,
		time=time,
		status=random.randint(1, 2)
	)

def create_appointmentnotes(appointment):
	return AppointmentNotes.objects.create(
		interview=faker.sentence(),
		recommendations=faker.sentence(),
		remarks=faker.sentence(),
		medications=faker.sentence(),
		diagnosis=faker.sentence(),
		appointment=appointment
	)