import random
import secrets
import string

from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import FormView, UpdateView, CreateView

from catalog.models import Product
from catalog.views import MyBaseFooter
from home_work_20_1.settings import EMAIL_HOST_USER
from user.forms import UserLoginForm
from .forms import RegistrationForm
from .models import CustomUser
import requests

response = requests.get('https://example.com', verify=True)  # Включена проверка сертификатов

class PasswordResetView(UpdateView):
    template_name = 'catalog/password_reset.html'
    form_class = PasswordResetForm
    success_url = reverse_lazy('user:login')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        user = CustomUser.objects.get(email=email)
        new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        user.password = make_password(new_password)
        user.save()

        send_mail(
            subject=f'Подтверждение регистрации',
            message=f'Для подтверждения регистрации перейдите по ссылке: {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )

        return super().form_valid(form)


class UserLoginView(MyBaseFooter, LoginView):
    template_name = 'catalog/login.html'
    form_class = UserLoginForm
    redirect_authenticated_user = True


class RegistrationView(CreateView):
    model = CustomUser
    template_name = 'catalog/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('user:login')

    def form_valid(self, form):
        """Отправка пользователю письма с подтверждением регистрации"""
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)  # генерит токен
        user.token = token
        user.save()
        host = self.request.get_host()  # это получение хоста
        url = f'http://{host}/user/verify/{token}'
        send_mail(
            subject=f'Подтверждение регистрации',
            message=f'Для подтверждения регистрации перейдите по ссылке: {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)

def verify_mail(request, token):
    """Подтверждение регистрации переход по ссылке из письма и редирект на страницу входа"""
    user = get_object_or_404(CustomUser, token=token)  # получить пользователя по токен
    user.is_active = True
    user.save()
    return redirect(reverse('user:login'))


class UserProfileView(MyBaseFooter, UpdateView):
    model = CustomUser
    template_name = 'catalog/user_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_products'] = Product.objects.filter(autor=self.object)
        return context
