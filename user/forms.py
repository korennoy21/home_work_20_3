from django import forms
from .models import CustomUser
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from user.models import CustomUser

from catalog.forms import CustomFormMixin




class UserLoginForm(CustomFormMixin, AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'password')


class UserProfileUpdateForm(CustomFormMixin, UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'avatar', 'phone_number',
                  'country', 'first_name', 'last_name', 'new_password'
                  )

    def __init__(self, *args, **kwargs):
        """Штука скрывает стандартное поле пароля"""
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()

class RegistrationForm(UserCreationForm):


    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2']

