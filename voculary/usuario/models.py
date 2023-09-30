from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, primeiro_nome, ultimo_nome, password=None):
        if not email:
            raise ValueError('O usuário deve ter um endereço de e-mail.')
        if not primeiro_nome:
            raise ValueError('O usuário deve ter um primeiro nome.')
        if not ultimo_nome:
            raise ValueError('O usuário deve ter um último nome.')

        email = self.normalize_email(email)
        usuario = self.model(
            email=email,
            primeiro_nome=primeiro_nome,
            ultimo_nome=ultimo_nome,
        )

        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, email, primeiro_nome, ultimo_nome, password=None):

        usuario = self.create_user(
            email=email,
            primeiro_nome=primeiro_nome,
            ultimo_nome=ultimo_nome,
            password=password
        )

        usuario.staff = True
        usuario.admin = True
        usuario.save(using=self._db)
        return usuario


class Usuario(AbstractBaseUser):
    primeiro_nome = models.CharField(max_length=100)
    ultimo_nome = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, unique=True)
    ativo = models.BooleanField(default=True)
    data_registro = models.DateTimeField(auto_now_add=True, null=False)
    ultimo_login = models.DateTimeField(blank=True, null=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['primeiro_nome', 'ultimo_nome']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    class Meta:
        db_table = 'usuario'