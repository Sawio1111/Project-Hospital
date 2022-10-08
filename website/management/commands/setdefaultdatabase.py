from .commands_utils import (
	create_admin_test, create_datetimework, create_qualification, create_service, create_opinion, create_patient,
	create_doctor, create_doctor_test, create_patient_test, create_appointment, create_appointmentnotes
							)
from django.core.management.base import BaseCommand


class Command(BaseCommand):
	help = 'Insert patients, doctors and admin to database'

	def handle(self, *args, **options):

		create_service('allergist')
		create_service('endocrinologist')
		create_service('first contact doctor')
		service_2 = create_service('neurologist')
		service = create_service('therapist')

		create_admin_test()
		create_patient_test()
		doctor = create_doctor_test()
		create_qualification(doctor, service)

		for i in range(5):
			patient = create_patient()
			for i in range(2):
				create_opinion(patient)
			doctor = create_doctor()
			create_qualification(doctor, service_2)
			create_datetimework(doctor)


