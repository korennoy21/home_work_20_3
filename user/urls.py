from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.urls import path

from user.apps import UserConfig
from .views import RegistrationView, UserLoginView, PasswordResetView , verify_mail

app_name = 'user'

urlpatterns = [
                  path('register/', RegistrationView.as_view(), name='register'),
                  path('logout/', LogoutView.as_view(), name='logout'),
                  path('verify/<str:token>', verify_mail, name='verify'),
                  path('login/', UserLoginView.as_view(), name='login'),
                  path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
