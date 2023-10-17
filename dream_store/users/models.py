from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin)


class MainUserManager(BaseUserManager):
    """
    Менеджер для пользователей.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Создает и возвращает пользователя c email и паролем.
        """

        if not email:
            raise ValueError('У пользователя должен быть email')

        user = self.model(
            email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        UserProfile.objects.create(user=user)

        return user

    def create_superuser(self, email, password=None):
        """
        Создает и возвращает супер-пользователя c email и паролем.
        """

        user = self.create_user(email, password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Облегченная модель для пользователя.
    """

    email = models.EmailField(
        verbose_name='Электронная почта',
        max_length=255,
        unique=True)
    is_active = models.BooleanField(
        verbose_name='Активен', default=True)
    is_staff = models.BooleanField(
        verbose_name='Персонал', default=False)
    date_joined = models.DateTimeField(
        verbose_name='Дата создания', default=timezone.now)

    objects = MainUserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('-id',)

    def __str__(self) -> str:
        return self.email


class UserProfile(models.Model):
    """
    Профиль пользователя с необходимыми полями.
    """

    user = models.OneToOneField(User,
                                verbose_name='Пользователь',
                                on_delete=models.CASCADE)
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=255,
        blank=True)
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=255,
        blank=True)
    about = models.TextField(
        verbose_name='О себе',
        max_length=500,
        blank=True)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self) -> str:
        return self.user.email
