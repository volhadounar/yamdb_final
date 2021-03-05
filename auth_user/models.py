from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class CustomUserManager(UserManager):
    """Менеджер пользователей."""
    def create_user(self, email, password=None, **extra_fields):
        """
        Создает объект пользвателя с указанным адресом
        электронной почты, датой рождения и паролем.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )
        if password:
            user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Создает объект суперпользвателя с указанным адресом
        электронной почты, датой рождения и паролем.
        """

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        user = self.create_user(
            email,
            password=password,
            **extra_fields
        )
        user.role = 'admin'
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):
    """Реализация User в виде абстрактной модели."""
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'

    ROLE_CHOICES = (
        (ADMIN, 'admin'),
        (MODERATOR, 'moderator'),
        (USER, 'user')
    )

    email = models.EmailField(
        verbose_name='email address',
        max_length=200,
        null=False,
        unique=True
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )
    bio = models.TextField(verbose_name='description', null=True, blank=True)
    first_name = models.CharField(verbose_name='first name', max_length=200,
                                  null=True, blank=True)
    last_name = models.CharField(verbose_name='last name', max_length=200,
                                 null=True, blank=True)

    REQUIRED_FIELDS = []
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    class Meta:
        ordering = ['email']

    def __str__(self):
        return self.email

    @property
    def is_admin(self):
        return True if self.role == self.ADMIN or self.is_staff else False

    @property
    def is_moderator(self):
        return True if self.role == self.MODERATOR else False

    @property
    def is_user(self):
        return True if self.role == self.USER else False
