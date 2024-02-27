from django import forms
from shopit.models import User

class UserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['firstname', 'lastname', 'username', 'email', 'password']