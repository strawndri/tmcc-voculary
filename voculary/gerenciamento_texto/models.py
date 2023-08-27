from django.db import models
from usuario.models import Usuario

from datetime import datetime

class Imagem(models.Model):
    id_imagem = models.AutoField(primary_key=True)
    arquivo = models.ImageField(upload_to='imagens/', null=False)
    ativo = models.BooleanField(null=False)

    usuario = models.ForeignKey(
        to = Usuario,
        on_delete = models.SET_NULL,
        null = True,
        related_name = 'imagem'
    )

    class Meta:
        db_table = 'imagem'

class TextoDigitalizado(models.Model):
    data_geracao = models.DateTimeField(default=datetime.now, null=False)
    texto = models.TextField(null=False)
    nome = models.CharField(max_length=255, null=False)
    tempo_processamento = models.FloatField(null=False)
    idioma = models.CharField(max_length=10, null=False)
    ativo = models.BooleanField(null=False)

    usuario = models.ForeignKey(
        to = Usuario,
        on_delete = models.SET_NULL,
        null = True,
        related_name = 'texto_digitalizado'
    )

    imagem = models.ForeignKey(
        to = Imagem,
        on_delete = models.SET_NULL,
        null = True,
        related_name = 'texto_digitalizado'
    )

    class Meta:
        db_table = 'texto_digitalizado'