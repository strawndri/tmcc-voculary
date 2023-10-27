from django.db import models
from usuario.models import User
from django.utils import timezone

class Image(models.Model):
    """
    Modelo para armazenar informações acerca das imagens enviadas pelos usuários.
    """
    image_id = models.AutoField(primary_key=True, verbose_name="ID da Imagem")
    file = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name="Arquivo")
    is_active = models.BooleanField(default=True, verbose_name="Ativo")

    user = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='image',
        verbose_name="Usuário"
    )

    class Meta:
        db_table = 'image'
        verbose_name = "Imagem"
        verbose_name_plural = "Imagens"

class DigitizedText(models.Model):
    """
    Modelo para armazenar informações relacionadas aos texto gerados a partir de imagens.
    """
    creation_date = models.DateTimeField(default=timezone.now, verbose_name="Data de Geração")
    text = models.TextField(verbose_name="Texto")
    name = models.CharField(max_length=255, verbose_name="Nome")
    processing_time = models.FloatField(verbose_name="Tempo de Processamento")
    language = models.CharField(max_length=10, verbose_name="Idioma")
    is_active = models.BooleanField(default=True, verbose_name="Ativo")

    user = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='digitized_text',
        verbose_name="Usuário"
    )

    image = models.OneToOneField(
        to=Image,
        on_delete=models.CASCADE,
        primary_key=True,  
        related_name='digitized_text',
        verbose_name="Imagem"
    )

    class Meta:
        db_table = 'digitized_text'
        verbose_name = "Texto Digitalizado"
        verbose_name_plural = "Textos Digitalizados"
