import datetime

from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.views.generic import CreateView, UpdateView, FormView, RedirectView, DeleteView, ListView
from django.contrib.auth.views import LoginView, LogoutView, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import (
	RegistrationForm, UpdateProfileForm, DoctorAccountWorkForm, ChooseServiceForm, CreateOpinionForm,
	CreateAppointmentNotesForm
)

from .models import DateTimeWork, Service, TimeAppointment, Appointment, Opinion, AppointmentNotes

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
		login(self.request, self.object)
		return response


class PatientAccountPanelView(LoginRequiredMixin, View):
	template_name = 'website/patient_panel.html'
	context = {}

	def get(self, request, *args, **kwargs):
		self.context['appointments'] = Appointment.objects.filter(patient_id=request.user.pk, status=1)
		return render(request, template_name=self.template_name, context=self.context)


class PatientAccountUpdateView(LoginRequiredMixin, UpdateView):
	template_name = 'website/patient_update.html'
	form_class = UpdateProfileForm
	success_url = reverse_lazy('patient-panel')

	def get_queryset(self):
		return User.objects.filter(pk=self.kwargs['pk'])


class PatientChooseServiceView(LoginRequiredMixin, View):
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


class PatientAppointmentCreateView(LoginRequiredMixin, RedirectView):
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


class PatientCancelAppointment(LoginRequiredMixin, DeleteView):
	template_name = 'website/patient_delete_appointment.html'
	success_url = reverse_lazy('patient-panel')
	queryset = Appointment.objects.all()


class PatientAddOpinion(LoginRequiredMixin, FormView):
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


class PatientListAppointmentView(LoginRequiredMixin, ListView):
	template_name = 'website/patient_timeline.html'

	def get_queryset(self):
		return Appointment.objects.filter(patient_id=self.kwargs['patient_pk'], status=2).order_by('date')


class DoctorAccountPanelView(LoginRequiredMixin, View):
	template_name = 'website/doctor_panel.html'

	def get(self, request, *args, **kwargs):
		if "today_appointment" in request.session:
			del request.session["today_appointment"]
		today_appointments = Appointment.objects.filter(doctor_id=request.user.pk, status=1).order_by('time')
		return render(request, template_name=self.template_name, context={'today_appointments': today_appointments})


class DoctorAccountWorkView(LoginRequiredMixin, FormView):
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


class DoctorPatientsView(LoginRequiredMixin, ListView):
	template_name = 'website/doctor_all_patients.html'
	ordering = ['patient']

	def get_queryset(self):
		queryset = Appointment.objects.filter(doctor=self.request.user).values_list('patient_id').distinct()
		unique_patient = [User.objects.get(pk=patient_id[0]) for patient_id in queryset]
		return unique_patient


class DoctorStartAppointmentView(LoginRequiredMixin, FormView):
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


class AdministratorAccountPanelView(LoginRequiredMixin, View):
	template_name = 'website/administrator_panel.html'

	def get(self, request, *args, **kwargs):
		return render(request, template_name=self.template_name)


class PrivacyAndRegulationView(View):
	template_name = 'website/privacy_policy_regulation.html'

	def get(self, request, *args, **kwargs):
		return render(request, self.template_name)


