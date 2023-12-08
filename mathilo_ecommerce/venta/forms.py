from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import PedidoPersonalizado

class CustomUserCreationForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
	def clean_email(self):
		email = self.cleaned_data['email']

		if User.objects.filter(email=email).exists():
			raise forms.ValidationError('Este correo electrónico ya está registrado')
		return email

class PedidoPersonalizadoForm(forms.ModelForm):
    class Meta:
        model = PedidoPersonalizado
        fields = ['mensaje', 'número_celular']
        widgets = {
            'mensaje': forms.Textarea(attrs={'rows': 7}),
        }

class UserPrefilForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
