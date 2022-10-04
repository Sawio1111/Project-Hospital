from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator


class User(AbstractUser):
	user_status = (
		(1, 'client'),
		(2, 'doctor'),
		(3, 'administrator'),
	)

	user_sex = (
		(1, 'female'),
		(2, 'male'),
	)

	pesel = models.IntegerField(null=True)
	sex = models.SmallIntegerField(null=True, choices=user_sex)
	phone_number = models.IntegerField(null=True)
	status = models.SmallIntegerField(default=1, choices=user_status)

	def __str__(self):
		return f"{self.first_name} {self.last_name}"


class Service(models.Model):
	name = models.CharField(max_length=64)
	description = models.TextField(null=True)

	def __str__(self):
		return self.name


class Qualification(models.Model):
	doctor = models.OneToOneField(User, on_delete=models.CASCADE)
	degree = models.CharField(max_length=64)
	service = models.ForeignKey(Service, null=True, on_delete=models.SET_NULL, related_name='service')
	salary = models.FloatField(default=0)
	price = models.FloatField(default=0)
	room = models.SmallIntegerField(null=True)


class DateTimeWork(models.Model):
	status = (
		(1, 'not approved'),
		(2, 'approved'),
	)

	doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_date_time_work')
	date_from = models.DateField()
	date_to = models.DateField()
	visit_time = models.SmallIntegerField()
	time_from = models.TimeField()
	time_to = models.TimeField()
	status = models.SmallIntegerField(default=1, choices=status)


class TimeAppointment(models.Model):
	date_time_work = models.ForeignKey(DateTimeWork, on_delete=models.CASCADE, related_name='date_time_work')
	visit_time = models.TimeField()


class Appointment(models.Model):
	status = (
		(1, 'created'),
		(2, 'confirmed'),
		(3, 'archived')
	)
	patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient_appointment')
	doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_appointment')
	date = models.DateField()
	time = models.TimeField()
	status = models.SmallIntegerField(default=1, choices=status)
	created = models.TimeField(auto_now_add=True, null=True)


class Opinion(models.Model):
	status = (
		(1, 'not approved'),
		(2, 'approved'),
	)

	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
	rating = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], null=False)
	description = models.CharField(max_length=2048, null=False)
	status = models.SmallIntegerField(default=1, choices=status)


