from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None  # Отключаем поле username

    first_name = models.CharField(verbose_name='Имя', max_length=30)
    last_name = models.CharField(verbose_name='Фамилия', max_length=30)  # Добавляем поле last_name
    email = models.EmailField(verbose_name='Почта', unique=True)
    avatar = models.ImageField(verbose_name='Аватар', upload_to='avatars/', **NULLABLE)
    phone_number = models.CharField(verbose_name='Телефон', max_length=15, **NULLABLE)
    country = models.CharField(verbose_name='Страна', max_length=100, **NULLABLE)
    token = models.CharField(max_length=255, **NULLABLE, verbose_name='Токен')
    new_password = models.CharField(verbose_name='Новый пароль', max_length=100, **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']  # Поле last_name включено

    objects = CustomUserManager()  # Используем кастомный менеджер
