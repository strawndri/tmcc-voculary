# Generated by Django 4.1.7 on 2023-10-08 11:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gerenciamento_texto', '0006_digitizedtext_image_remove_textodigitalizado_imagem_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='digitizedtext',
            name='id',
        ),
        migrations.AlterField(
            model_name='digitizedtext',
            name='image',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='digitized_text', serialize=False, to='gerenciamento_texto.image', verbose_name='Imagem'),
        ),
    ]
