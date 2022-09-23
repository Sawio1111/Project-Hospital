from django.shortcuts import render
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from django.views.generic import CreateView, UpdateView, FormView
from django.contrib.auth.views import LoginView, LogoutView, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import RegistrationForm, UpdateProfileForm


User = get_user_model()


class MainPageView(View):
	template_name = 'website/main_page.html'

	def get(self, request, *args, **kwargs):
		return render(request, template_name=self.template_name)


class LoginToWebsiteView(LoginView):
	template_name = 'website/login.html'


class LogoutFromWebsiteView(LoginRequiredMixin, LogoutView):
	template_name = 'website/logout.html'


class RegistrationView(CreateView):
	template_name = 'website/registration.html'
	model = User
	form_class = RegistrationForm

	def form_valid(self, form):
		response = super().form_valid(form)
		cd = form.cleaned_data
		self.object.set_password(cd['password1'])
		self.object.save()
		login(self.request, self.object)
		return response

	def get_success_url(self):
		return reverse_lazy('patient-panel')


class PatientAccountPanelView(LoginRequiredMixin, View):
	template_name = 'website/patient_account_panel.html'

	def get(self, request, *args, **kwargs):
		user = User.objects.get(pk=request.user.pk)
		return render(request, template_name=self.template_name, context={'user': user})


class PatientAccountUpdateView(LoginRequiredMixin, UpdateView):
	template_name = 'website/patient_account_update.html'
	form_class = UpdateProfileForm
	success_url = reverse_lazy('patient-panel')

	def get_queryset(self):
		return User.objects.filter(pk=self.kwargs['pk'])

