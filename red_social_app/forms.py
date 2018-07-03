from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class formularioregistro(forms.Form):


	username = forms.CharField(label='Usuario', widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
	first_name = forms.CharField(label='Nombre', widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
	last_name = forms.CharField(label='Apellidos', widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
	email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'class': 'form-control'}))
	password = forms.CharField(label='Contrasena', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
	repite_password = forms.CharField(label='Repite Contrasena', widget=forms.PasswordInput(attrs={'class': 'form-control'}))



	def clean_email(self):

		email = self.cleaned_data['email']

		if User.objects.filter(email=email).exists():

			raise ValidationError('el email indicado ya tiene una cuenta asociada')

		return email


class formularioactualizar(forms.ModelForm):

	class Meta:

		model = User
		fields = ['username', 'first_name', 'last_name', 'email']
		



