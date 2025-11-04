from django.db import models
from django.contrib.auth.models import AbstractUser
import secrets
from datetime import timedelta
from django.utils import timezone
import os

class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_registered = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # Добавьте эти поля для разрешения конфликта
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',  # Уникальное имя
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',  # Уникальное имя
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

class Token(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, unique=True)
    expires_at = models.DateTimeField()
    token_type = models.CharField(max_length=20, choices=[('register', 'Register'), ('reset', 'Reset')])

    @staticmethod
    def generate_token(user, token_type):
        token = secrets.token_urlsafe(32)
        expiry = timezone.now() + timedelta(minutes=int(os.getenv('TOKEN_EXPIRY_MINUTES', 2880)))
        Token.objects.create(user=user, token=token, expires_at=expiry, token_type=token_type)
        print(token)
        return token