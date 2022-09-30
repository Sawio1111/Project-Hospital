import datetime

from django import forms
from django.contrib.auth import get_user_model
from django.core.validators import ValidationError

from .models import DateTimeWork, Qualification, Service
from .widget import DatePickerInput, TimePickerInput

User = get_user_model()


class RegistrationForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['last_name'].required = True
		self.fields['first_name'].required = True
		self.fields['email'].required = True
		self.fields['sex'].required = True

	password1 = forms.CharField(
		widget=forms.PasswordInput,
		required=True,
		label="Password"
	)
	password2 = forms.CharField(
		widget=forms.PasswordInput,
		required=True,
		label="Repeat Password",
		help_text='Password should have more than 8 characters'
	)
	contract = forms.CharField(
		widget=forms.CheckboxInput,
		required=True,
		label="Consent to the terms of Regulations and Privacy Policy (required)."
	)

	class Meta:
		model = User
		fields = [
			'first_name',
			'last_name',
			'username',
			'phone_number',
			'pesel',
			'sex',
			'email',
			'password1',
			'password2',
			'contract'
		]

		help_texts = {
			'username': 'Username should have more than 4 characters',
		}

		widgets = {
			'phone_number': forms.TextInput(),
			'pesel': forms.TextInput(),
		}

	def clean(self):
		form = super().clean()
		password1 = form.get('password1')
		password2 = form.get('password2')
		username = form.get('username')

		if password1 != password2:
			raise ValidationError("Passwords are not the same")

		if len(password1) < 8:
			raise ValidationError('Password should have more than 8 characters')

		if len(username) < 4:
			raise ValidationError('Username should have more than 4 characters')


class UpdateProfileForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['email'].required = True

	class Meta:
		model = User
		fields = [
			'username',
			'phone_number',
			'email'
		]

		widgets = {
			'phone_number': forms.TextInput(),
		}


class ChooseServiceForm(forms.Form):
	service = forms.ModelChoiceField(queryset=Service.objects.all(), required=True)
	visit_date = forms.DateField(widget=DatePickerInput, required=True)

	def clean(self):
		form = super().clean()
		visit_date = form.get('visit_date')

		if datetime.date.today() > visit_date:
			raise ValidationError("This date has already been")


class DoctorAccountWorkForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		super().__init__(*args, **kwargs)

	class Meta:
		model = DateTimeWork
		fields = [
			'date_from',
			'date_to',
			'time_from',
			'time_to',
			'visit_time',
		]

		labels = {
			'date_from': "From (date)",
			'date_to': "Until (date)",
			'time_from': "From (time of the day)",
			'time_to': "Until (time of the day)",
		}

		widgets = {
			'date_from': DatePickerInput(),
			'date_to': DatePickerInput(),
			'time_from': TimePickerInput(),
			'time_to': TimePickerInput(),
			'visit_time': forms.TextInput(attrs={'placeholder': 'minutes'})
		}

	def clean(self):
		form = super().clean()
		date_from = form.get('date_from')
		date_to = form.get('date_to')
		time_from = form.get('time_from')
		time_to = form.get('time_to')
		visit_time = form.get('visit_time')

		if date_from > date_to:
			raise ValidationError("Wrong dates")

		if time_from >= time_to:
			raise ValidationError("Wrong times")

		if datetime.date.today() > date_from:
			raise ValidationError("This day has already been")

		if visit_time < 0 or visit_time > 55:
			raise ValidationError("Time of visit should be between 0 and 55 min")

		if DateTimeWork.objects.filter(date_from=date_from, doctor_id=self.request.user.pk) or \
				DateTimeWork.objects.filter(date_to=date_to, doctor_id=self.request.user.pk) or \
				DateTimeWork.objects.filter(date_from=date_to, doctor_id=self.request.user.pk):
			raise ValidationError("Working times is already set")
