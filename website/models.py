from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
	user_status = (
		(1, 'client'),
		(2, 'doctor'),
		(3, 'administrator'),
	)

	pesel = models.IntegerField(null=True)
	phone_number = models.IntegerField(null=True)
	status = models.SmallIntegerField(default=1, choices=user_status)


