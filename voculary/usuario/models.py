from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError('O usuário deve ter um endereço de e-mail.')
        if not first_name:
            raise ValueError('O usuário deve ter um primeiro nome.')
        if not last_name:
            raise ValueError('O usuário deve ter um último nome.')

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None):

        user = self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )

        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    first_name = models.CharField(max_length=100, verbose_name="Primeiro Nome")
    last_name = models.CharField(max_length=100, verbose_name="Último Nome")
    email = models.EmailField(max_length=255, unique=True, verbose_name="E-mail")
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    date_registered = models.DateTimeField(auto_now_add=True, verbose_name="Data de Registro")
    is_staff = models.BooleanField(default=False, verbose_name="É Staff?")
    is_admin = models.BooleanField(default=False, verbose_name="É Admin?")

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    class Meta:
        db_table = 'user'
