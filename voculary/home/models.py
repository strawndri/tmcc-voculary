from django.db import models
from usuario.models import CustomUser

from datetime import datetime

class Imagem(models.Model):
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    id_imagem = models.AutoField(primary_key=True) # chave primária
    imagem = models.ImageField(upload_to='imagens/', blank=True)

class ArquivoDigitalizado(models.Model):
    id_arquivo = models.AutoField(primary_key=True)
    data_geracao = models.DateTimeField(default=datetime.now, blank=False)
    tempo_processamento = models.FloatField(blank=False)
    acuracia = models.DecimalField(max_digits=6, decimal_places=2, blank=False)
    nome_arquivo = models.CharField(max_length=150, blank=False)

    usuario = models.ForeignKey(
        to = CustomUser,
        on_delete = models.SET_NULL,
        null = True,
        blank = False,
        related_name = 'user'
    )

    imagem = models.ForeignKey(
        to = Imagem,
        on_delete = models.SET_NULL,
        null = True,
        blank = False,
        related_name = 'image'
    )