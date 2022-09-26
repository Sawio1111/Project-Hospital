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

