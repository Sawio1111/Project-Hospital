import datetime

from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.models import Permission
from django.views.generic import CreateView, UpdateView, FormView, RedirectView, DeleteView, ListView
from django.contrib.auth.views import (
	LoginView, LogoutView, get_user_model, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin

from .forms import (
	RegistrationForm, UpdateProfileForm, DoctorAccountWorkForm, ChooseServiceForm, CreateOpinionForm,
	CreateAppointmentNotesForm, CreateDoctorForm, SearchPatientForm
)
from .models import DateTimeWork, Service, TimeAppointment, Appointment, Opinion, AppointmentNotes, Qualification

User = get_user_model()


class MainPageView(View):
	template_name = 'website/main_page.html'
	context = {}

	def get(self, request, *args, **kwargs):
		services = Service.objects.filter().order_by('?')[:4]
		if len(services) >= 4:
			self.context['services'] = services
		opinions = Opinion.objects.filter(status=2).order_by('?')[:3]
		if len(opinions) >= 3:
			self.context['opinions'] = opinions

		return render(request, template_name=self.template_name, context=self.context)


class LoginToWebsiteView(LoginView):
	template_name = 'website/login.html'
	next_page = None

	def form_valid(self, form):
		user = form.get_user()
		if user.status == 1:
			self.next_page = reverse_lazy('patient-panel')
		if user.status == 2:
			self.next_page = reverse_lazy('doctor-panel')
		if user.status == 3:
			self.next_page = reverse_lazy('admin-panel')
		return super().form_valid(form)


class LogoutFromWebsiteView(LoginRequiredMixin, LogoutView):
	template_name = 'website/logout.html'


class RegistrationView(CreateView):
	template_name = 'website/registration.html'
	model = User
	form_class = RegistrationForm
	success_url = reverse_lazy('patient-panel')

	def form_valid(self, form):
		response = super().form_valid(form)
		cd = form.cleaned_data
		self.object.set_password(cd['password1'])
		self.object.save()
		permission = Permission.objects.get(codename='client_permission')
		self.object.user_permissions.add(permission)
		login(self.request, self.object)
		return response


class ResetPasswordView(PasswordResetView):
	template_name = 'website/reset_password.html'
	initial = {
	}

	def get(self, request, *args, **kwargs):
		if "doctor_email" in request.session:
			self.initial['email'] = request.session['doctor_email']
			self.email_template_name = 'website/doctor_set_password.html'
		return super().get(self, request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		if "doctor_email" in request.session:
			self.email_template_name = 'website/doctor_set_password.html'
		return super().post(self, request, *args, **kwargs)


class ResetPasswordDoneView(PasswordResetDoneView):
	template_name = 'website/reset_password_done.html'


class ResetPasswordConfirmView(PasswordResetConfirmView):
	template_name = 'website/reset_password_confirm.html'
	success_url = reverse_lazy('main')


class PatientAccountPanelView(PermissionRequiredMixin, View):
	permission_required = 'website.client_permission'
	template_name = 'website/patient_panel.html'
	context = {}

	def get(self, request, *args, **kwargs):
		self.context['appointments'] = Appointment.objects.filter(patient_id=request.user.pk, status=1)
		return render(request, template_name=self.template_name, context=self.context)


class PatientAccountUpdateView(PermissionRequiredMixin, UserPassesTestMixin, UpdateView):
	permission_required = 'website.client_permission'

	def test_func(self):
		return self.request.user == User.objects.get(pk=self.kwargs['pk'])

	template_name = 'website/patient_update.html'
	form_class = UpdateProfileForm
	success_url = reverse_lazy('patient-panel')

	def get_queryset(self):
		return User.objects.filter(pk=self.kwargs['pk'])


class PatientChooseServiceView(PermissionRequiredMixin, View):
	permission_required = 'website.client_permission'
	template_name = 'website/patient_choose.html'
	form_class = ChooseServiceForm

	def get(self, request, *args, **kwargs):
		form = self.form_class()
		return render(request, self.template_name, context={'form': form})

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			service = cd['service']
			visit_date = cd["visit_date"]
			print(visit_date)
			visits_allowed = DateTimeWork.objects.filter(
				date_from__lte=visit_date,
				date_to__gte=visit_date,
				doctor__qualification__service=service,
				status=2
			)
			visit_context = {}
			for date_time_work in visits_allowed:
				time_visit = TimeAppointment.objects.filter(date_time_work_id=date_time_work.pk)
				appointments_booked = [i.strftime("%H:%M")
									 for i in
									 Appointment.objects.filter(doctor_id=date_time_work.doctor.pk, date=visit_date).values_list('time', flat=True)
									 ]
				list_time= []
				for time in time_visit:
					if time.visit_time.strftime("%H:%M") not in appointments_booked:
						list_time.append(time.visit_time.strftime("%H:%M"))
				visit_context[date_time_work.doctor] = list_time
			return render(request, self.template_name, context={
				'form': form,
				'visit_context': visit_context,
				'date': visit_date.strftime("%Y:%m:%d")
			})
		return render(request, self.template_name, context={'form': form})


class PatientAppointmentCreateView(PermissionRequiredMixin, RedirectView):
	permission_required = 'website.client_permission'

	url = reverse_lazy('patient-panel')

	def get(self, request, *args, **kwargs):
		date = datetime.datetime.strptime(kwargs['date_visit'], '%Y:%m:%d')
		time_visit = kwargs['time']
		doctor = kwargs['doctor_pk']
		service = kwargs['service_pk']
		date_time_work = DateTimeWork.objects.filter(
				date_from__lte=date,
				date_to__gte=date,
				doctor__qualification__service_id=service,
				doctor_id=doctor,
				status=2
			)
		if date_time_work:
			time_appointment = TimeAppointment.objects.filter(date_time_work=date_time_work[0])
			appointment = Appointment.objects.filter(
				patient_id=request.user.pk,
				doctor__qualification__service_id=service,
				status=1
			)
			for time in time_appointment:
				if time_visit in time.visit_time.strftime("%H:%M"):
					if not appointment:
						Appointment.objects.create(
							date=date,
							time=time_visit,
							doctor_id=doctor,
							patient_id=request.user.pk
						)
		return super().get(self, request, *args, **kwargs)


class PatientCancelAppointment(PermissionRequiredMixin, DeleteView):
	permission_required = 'website.client_permission'
	template_name = 'website/patient_delete_appointment.html'
	success_url = reverse_lazy('patient-panel')
	queryset = Appointment.objects.all()


class PatientAddOpinion(PermissionRequiredMixin, FormView):
	permission_required = 'website.client_permission'
	template_name = 'website/patient_opinion.html'
	form_class = CreateOpinionForm
	success_url = reverse_lazy('patient-panel')

	def form_valid(self, form):
		response = super().form_valid(form)
		cd = form.cleaned_data
		rating = cd['rating']
		description = cd['description']

		Opinion.objects.create(
			rating=rating,
			description=description,
			author_id=self.request.user.pk,
		)
		return response


class PatientListAppointmentView(PermissionRequiredMixin, ListView):
	permission_required = 'website.doctor_permission'
	template_name = 'website/patient_timeline.html'

	def get_queryset(self):
		return Appointment.objects.filter(patient_id=self.kwargs['patient_pk'], status=2).order_by('date')


class DoctorAccountPanelView(PermissionRequiredMixin, View):
	permission_required = 'website.doctor_permission'

	template_name = 'website/doctor_panel.html'

	def get(self, request, *args, **kwargs):
		if "today_appointment" in request.session:
			del request.session["today_appointment"]
		today_appointments = Appointment.objects.filter(
			doctor_id=request.user.pk,
			status=1,
			date=timezone.localtime(timezone.now())
		).order_by('time')
		return render(request, template_name=self.template_name, context={'today_appointments': today_appointments})


class DoctorAccountWorkView(PermissionRequiredMixin, FormView):
	permission_required = 'website.doctor_permission'
	template_name = 'website/doctor_work_set.html'
	form_class = DoctorAccountWorkForm
	model = DateTimeWork
	extra_context = {
	}
	success_url = reverse_lazy('doctor-work')

	def get(self, request, *args, **kwargs):
		self.extra_context['appointments'] = DateTimeWork.objects.filter(doctor_id=self.request.user.pk)
		return super().get( request, *args, **kwargs)

	def get_form_kwargs(self):
		form_kwargs = super().get_form_kwargs()
		form_kwargs['request'] = self.request
		return form_kwargs

	def form_valid(self, form):
		cd = form.cleaned_data
		doctor = User.objects.get(pk=self.request.user.pk)
		date_from = cd['date_from']
		date_to = cd['date_to']
		time_from = cd['time_from']
		time_to = cd['time_to']
		visit_time = cd['visit_time']
		date_time_work = DateTimeWork.objects.create(
			doctor=doctor,
			date_from=date_from,
			date_to=date_to,
			time_from=time_from,
			time_to=time_to,
			visit_time=visit_time
		)
		time_from = datetime.datetime.combine(datetime.datetime.today(), time_from)
		time_to = datetime.datetime.combine(datetime.datetime.today(), time_to)
		new_time = time_from
		while new_time <= time_to:
			if '13' not in new_time.strftime('%H:%M'):
				TimeAppointment.objects.create(
					date_time_work=date_time_work,
					visit_time=new_time
				)
			new_time = new_time + datetime.timedelta(minutes=visit_time)
		return super().form_valid(form)


class DoctorPatientsView(PermissionRequiredMixin, ListView):
	permission_required = 'website.doctor_permission'
	template_name = 'website/doctor_all_patients.html'
	ordering = ['patient']

	def get_queryset(self):
		queryset = Appointment.objects.filter(doctor=self.request.user).values_list('patient_id').distinct()
		unique_patient = [User.objects.get(pk=patient_id[0]) for patient_id in queryset]
		return unique_patient


class DoctorStartAppointmentView(PermissionRequiredMixin, FormView):
	permission_required = 'website.doctor_permission'
	template_name = 'website/start_appointment.html'
	form_class = CreateAppointmentNotesForm
	success_url = reverse_lazy('doctor-panel')
	extra_context = {}

	def get(self, request, *args, **kwargs):
		appointment = get_object_or_404(Appointment, pk=self.kwargs['appointment_pk'])
		self.extra_context['appointment'] = appointment
		request.session['today_appointment'] = appointment.pk
		return super().get(self, request, *args, **kwargs)

	def form_valid(self, form):
		cd = form.cleaned_data
		appointment_pk = self.kwargs['appointment_pk']
		appointment = get_object_or_404(Appointment, pk=appointment_pk)
		appointment.status = 2
		appointment.save()

		AppointmentNotes.objects.create(
			appointment=appointment,
			interview=cd['interview'],
			diagnosis=cd['diagnosis'],
			recommendations=cd['recommendations'],
			medications=cd['medications'],
			remarks=cd['remarks'],
		)
		return super().form_valid(form)


class DoctorEndAppointmentView(PermissionRequiredMixin, RedirectView):
	permission_required = 'website.doctor_permission'
	url = reverse_lazy('doctor-panel')

	def get(self, request, *args, **kwargs):
		appointment = get_object_or_404(Appointment, pk=self.kwargs['appointment_pk'])
		appointment.status = 3
		appointment.save()
		return super().get(self, request, *args, **kwargs)


class AdministratorAccountPanelView(PermissionRequiredMixin, View):
	permission_required = 'website.administrator_permission'
	template_name = 'website/admin_panel.html'

	def get(self, request, *args, **kwargs):
		return render(request, template_name=self.template_name)


class AdministratorCreateServiceView(PermissionRequiredMixin, CreateView):
	permission_required = 'website.administrator_permission'
	template_name = 'website/admin_create_service.html'
	model = Service
	fields = [
		'name',
		'description'
	]
	extra_context = {}
	success_url = reverse_lazy('admin-create-service')

	def get(self, request, *args, **kwargs):
		services = Service.objects.all().order_by('-created')
		self.extra_context['services'] = services
		return super().get(self, request, *args, **kwargs)


class AdministratorDeleteServiceView(PermissionRequiredMixin, DeleteView):
	permission_required = 'website.administrator_permission'
	template_name = 'website/admin_delete_service.html'
	model = Service
	success_url = reverse_lazy('admin-create-service')


class AdministratorListOpinionsView(PermissionRequiredMixin, ListView):
	permission_required = 'website.administrator_permission'
	template_name = 'website/admin_opinions.html'
	queryset = Opinion.objects.all()
	paginate_by = 5
	ordering = ['-created']


class AdministratorOpinionStatusView(PermissionRequiredMixin, RedirectView):
	permission_required = 'website.administrator_permission'

	def get(self, request, *args, **kwargs):
		opinion = get_object_or_404(Opinion, pk=self.kwargs['opinion_pk'])
		if opinion.status == 1:
			opinion.status = 2
			opinion.save()
		elif opinion.status == 2:
			opinion.status = 1
			opinion.save()
		return super().get(self, request, *args, **kwargs)

	def get_redirect_url(self, *args, **kwargs):
		return reverse_lazy('admin-list-opinions') + "#" + str(self.kwargs['opinion_pk'])


class AdministratorListDoctorView(PermissionRequiredMixin, ListView):
	permission_required = 'website.administrator_permission'
	template_name = 'website/admin_doctors.html'
	queryset = User.objects.filter(status=2)
	ordering = ['last_name']
	paginate_by = 25


class AdministratorDoctorUpdateView(PermissionRequiredMixin, UpdateView):
	permission_required = 'website.administrator_permission'
	template_name = 'website/doctor_update.html'
	success_url = reverse_lazy('admin-panel')
	fields = [
			'first_name',
			'last_name',
			'username',
			'phone_number',
			'pesel',
			'sex',
			'email',
	]

	def get_queryset(self):
		return User.objects.filter(pk=self.kwargs['pk'], status=2)


class AdministratorQualificationUpdateView(PermissionRequiredMixin, UpdateView):
	permission_required = 'website.administrator_permission'
	template_name = 'website/qualification_update.html'
	success_url = reverse_lazy('admin-panel')
	model = Qualification
	fields = [
		'salary',
		'price',
		'degree',
		'service',
		'room',
	]


class AdministratorCreateDoctorView(PermissionRequiredMixin, FormView):
	permission_required = 'website.administrator_permission'
	template_name = 'website/admin_create_doctor.html'
	form_class = CreateDoctorForm
	success_url = reverse_lazy('reset_password')

	def form_valid(self, form):
		cd = form.cleaned_data
		doctor = User.objects.create(
			last_name=cd['last_name'],
			first_name=cd['first_name'],
			email=cd['email'],
			pesel=cd['pesel'],
			phone_number=cd['phone_number'],
			sex=cd['sex'],
			username=cd['username'],
			status=2
		)
		permission = Permission.objects.get(codename='doctor_permission')
		doctor.user_permissions.add(permission)
		Qualification.objects.create(
			salary=cd['salary'],
			price=cd['price'],
			degree=cd['degree'],
			service=cd['service'],
			room=cd['room'],
			doctor=doctor,
		)
		self.request.session['doctor_email'] = cd['email']
		return super().form_valid(form)


class AdministratorUpdatePatientView(PermissionRequiredMixin, UpdateView):
	permission_required = 'website.administrator_permission'
	template_name = 'website/update_patient.html'
	success_url = reverse_lazy('admin-search-patient')
	fields = [
		'first_name',
		'last_name',
		'pesel',
		'sex',
	]

	def get_queryset(self):
		return User.objects.filter(pk=self.kwargs['pk'], status=1)


class AdministratorListPatientView(PermissionRequiredMixin, View):
	permission_required = 'website.administrator_permission'
	template_name = 'website/patient_list.html'
	form_class = SearchPatientForm

	def get(self, request, *args, **kwargs):
		form = self.form_class()
		return render(request, self.template_name, context={'form': form})

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		users = None
		if form.is_valid():
			cd = form.cleaned_data
			if cd['last_name'] == None:
				cd['last_name'] = ''
			if cd['pesel'] == None:
				cd['pesel'] = ''
			users = User.objects.filter(last_name__icontains=cd['last_name'], pesel__icontains=cd['pesel'], status=1)
		return render(request, self.template_name, context={'users': users, 'form': form})


class AdministratorDoctorWorkView(PermissionRequiredMixin, RedirectView):
	permission_required = 'website.administrator_permission'
	url = reverse_lazy('admin-list-doctors')

	def get(self, request, *args, **kwargs):
		date_work_time = get_object_or_404(DateTimeWork, pk=self.kwargs['date_pk'])
		if date_work_time.status == 1:
				date_work_time.status = 2
				date_work_time.save()
		elif date_work_time.status == 2:
			date_work_time.status = 1
			date_work_time.save()
		return super().get(self, request, *args, **kwargs)


class PrivacyAndRegulationView(View):
	template_name = 'website/privacy_policy_regulation.html'

	def get(self, request, *args, **kwargs):
		return render(request, self.template_name)


