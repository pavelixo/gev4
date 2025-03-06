from decimal import Decimal
from django.db import models
from django.utils.translation import gettext_lazy as _
from .base import AbstractUser, AbstractUserManager


class UserManager(AbstractUserManager):

    def _create_user(
            self,
            username,
            email,
            password,
            **extra_fields
          ):

        if not username:
            raise ValueError(
              _('Username field must be set')
            )

        if not email:
            raise ValueError(
                _('Email field must be set')
            )

        email = self.normalize_email(email)
        username = self.normalize_username(username)

        user = self.model(
            username=username,
            display_username=username,
            email=email,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_user(
            self,
            username,
            email=None,
            password=None,
            **extra_fields
          ):

        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(
            self,
            username,
            email=None,
            password=None,
            **extra_fields
          ):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)


class User(AbstractUser):

    display_username = models.CharField(
        _('display username'),
        max_length=64,
        editable=True,
        blank=False
    )

    balance = models.DecimalField(
        _('balance'),
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        editable=True,
        blank=False
    )

    objects = UserManager()

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
