from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    """
    Gerenciador personalizado para criar usuários e superusuários usando o 
    e-mail como campo de login.
    """

    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        """Cria e retorna um usuário.

        :param email: e-mail do usuário, o qual será utilizado durante a autenticação.
        :param first_name: primeiro nome do usuário.
        :param last_name: último nome (sobrenome) do usuário.
        :param password: senha do usuário, a qual será utilizada durante a autenticação.
        """
        
        if not email:
            raise ValueError('O usuário deve ter um endereço de e-mail.')
        
        email = self.normalize_email(email)
        
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    

    def create_superuser(self, email, first_name, last_name, password=None):
        """Cria e retorna um superusuário (administrador).

        :param email: e-mail do administrador, o qual será utilizado durante a autenticação.
        :param first_name: primeiro nome do administrador.
        :param last_name: último nome (sobrenome) do administrador.
        :param password: senha do administrador, a qual será utilizada durante a autenticação.
        """
        return self.create_user(email, first_name, last_name, password, is_staff=True, is_admin=True)


class User(AbstractBaseUser):
    """
    Modelo personalizado de usuário.
    """
    first_name = models.CharField(max_length=100, verbose_name="Primeiro Nome")
    last_name = models.CharField(max_length=100, verbose_name="Último Nome")
    email = models.EmailField(max_length=255, unique=True, verbose_name="E-mail")
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="Data de Registro")
    is_staff = models.BooleanField(default=False, verbose_name="É Staff?")
    is_admin = models.BooleanField(default=False, verbose_name="É Admin?")

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email


    @property
    def is_superuser(self):
        """Determine se o usuário é um superadministrador."""
        return self.is_admin
    

    def has_perm(self, perm, obj=None):
        """Verifica se o usuário tem permissão específica."""
        return True

    
    def has_module_perms(self, app_label):
        """Verifica se o usuário tem permissões para o app."""
        return True

    class Meta:
        db_table = 'user'