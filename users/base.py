from functools import reduce
from django.db import models
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin, BaseUserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from contrib.validators import TextValidator


class AbstractUserManager(BaseUserManager):
    @classmethod
    def normalize_username(cls, username):
        normalization_functions = [
            lambda string: string.strip(),
            lambda string: string.lower(),
        ]

        normalized_username = reduce(
            lambda acc, func: func(acc),
            normalization_functions, username
        )

        return normalized_username


class AbstractUser(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True

    username_validator = TextValidator()
    username = models.CharField(
        _('username'),
        max_length=32,
        unique=True,
        help_text=_(
            'Required. 32 characters or fewer.'
            'Letters, digits and @/./+/-/_ only.'
        ),
        validators=[username_validator],
        error_messages={
            'unique': _(
                'A user with that username already exists.'
            )
        }
    )

    email = models.EmailField(
        _('email address'),
        unique=True,
        blank=False
    )

    is_staff = models.BooleanField(
        _('is staff'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'
        )
    )

    is_active = models.BooleanField(
        _('is active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        )
    )

    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Send an email to this user.
        This method provides a convenient way to send emails to users,
        leveraging Django's send_mail function.
        """

        send_mail(subject, message, from_email, [self.email], **kwargs)