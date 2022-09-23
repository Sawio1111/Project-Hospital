from django import forms
from django.forms import TextInput
from django.contrib.auth import get_user_model
from django.core.validators import ValidationError

User = get_user_model()


class RegistrationForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['last_name'].required = True
		self.fields['first_name'].required = True
		self.fields['email'].required = True

	password1 = forms.CharField(widget=forms.PasswordInput,
								required=True,
								label="Password")
	password2 = forms.CharField(widget=forms.PasswordInput,
								required=True,
								label="Repeat Password",
								help_text='Password should have more than 8 characters')
	contract = forms.CharField(widget=forms.CheckboxInput,
							   required=True,
							   label='Consent to the terms of Regulations and Privacy Policy (required).'
									 '<p>Read the full text of the <a href="#" class="link-dark">'
									 'Privacy Policy and Regulations</a>')

	class Meta:
		model = User
		fields = ['first_name',
				  'last_name',
				  'username',
				  'phone_number',
				  'pesel',
				  'email',
				  'password1',
				  'password2',
				  'contract']

		help_texts = {
			'username': 'Username should have more than 4 characters',
		}

		widgets = {
			'phone_number': TextInput(),
			'pesel': TextInput(),
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
		self.fields['last_name'].required = True
		self.fields['first_name'].required = True
		self.fields['email'].required = True

	class Meta:
		model = User
		fields = ['first_name',
				  'last_name',
				  'username',
				  'phone_number',
				  'pesel',
				  'email']

		widgets = {
			'phone_number': TextInput(),
			'pesel': TextInput(),
		}