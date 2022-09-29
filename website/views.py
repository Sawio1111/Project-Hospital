import datetime

from django.shortcuts import render
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from django.views.generic import CreateView, UpdateView, FormView
from django.contrib.auth.views import LoginView, LogoutView, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import RegistrationForm, UpdateProfileForm, DoctorAccountWorkForm, ChooseServiceForm
from .models import DateTimeWork, Qualification

User = get_user_model()


class MainPageView(View):
	template_name = 'website/main_page.html'

	def get(self, request, *args, **kwargs):
		return render(request, template_name=self.template_name)


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

	def get(self, request, *args, **kwargs):
		return render(request, template_name=self.template_name)


class PatientAccountUpdateView(LoginRequiredMixin, UpdateView):
	template_name = 'website/patient_update.html'
	form_class = UpdateProfileForm
	success_url = reverse_lazy('patient-panel')

	def get_queryset(self):
		return User.objects.filter(pk=self.kwargs['pk'])


class PatientChooseServiceView(LoginRequiredMixin, View):
	template_name = 'website/patient_choose.html'
	form_class = ChooseServiceForm
	# model = Qualification
	# success_url = reverse_lazy('patient-choose')
	# extra_context = {
	# }

	def get(self, request, *args, **kwargs):
		form = self.form_class()
		return render(request, self.template_name, context={'form': form})

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			service = cd['service']
			visit_date = cd["visit_date"]
			visits_allowed = DateTimeWork.objects.filter(
				date_from__lte=visit_date,
				date_to__gte=visit_date,
				doctor__qualification__service=service,
				status=2
			)
			return render(request, self.template_name, context={
				'form': form,
				'visit_allowed': visits_allowed}
						  )
		return render(request, self.template_name, context={'form': form})


class DoctorAccountPanelView(LoginRequiredMixin, View):
	template_name = 'website/doctor_panel.html'

	def get(self, request, *args, **kwargs):
		return render(request, template_name=self.template_name)


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

	def form_valid(self, form):
		cd = form.cleaned_data
		doctor = User.objects.get(pk=self.request.user.pk)
		DateTimeWork.objects.create(
			doctor=doctor,
			date_from=cd['date_from'],
			date_to=cd['date_to'],
			time_from=cd['time_from'],
			time_to=cd['time_to'],
			visit_time=cd['visit_time']
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


