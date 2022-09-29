from django.db import models
from django.contrib.auth.models import AbstractUser


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


class DateTimeWork(models.Model):
	status = (
		(1, 'not approved'),
		(2, 'approved'),
	)

	doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor')
	date_from = models.DateField(null=False)
	date_to = models.DateField(null=False)
	visit_time = models.SmallIntegerField(null=False)
	time_from = models.TimeField(null=False)
	time_to = models.TimeField(null=False)
	status = models.SmallIntegerField(default=1, choices=status)