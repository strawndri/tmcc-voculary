from django.contrib import admin
from django.contrib.admin import AdminSite
from django.shortcuts import render
from .models import Usuario
from gerenciamento_texto.models import TextoDigitalizado
from django.db import models
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, F

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'primeiro_nome', 'ultimo_nome', 'email', 'ativo', 'data_registro')
    list_display_links = ('id', 'primeiro_nome', 'ultimo_nome')
    search_fields = ('primeiro_nome', 'ultimo_nome', 'email')
    list_filter = ('ativo', 'staff', 'admin')
    list_editable = ('ativo',)
    list_per_page = 10

admin.site.register(Usuario, UsuarioAdmin)

class CustomAdminSite(AdminSite):
    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['total_textos'] = str(TextoDigitalizado.objects.count()).zfill(2)
        extra_context['tempo_medio_processamento'] = str(round(TextoDigitalizado.objects.all().aggregate(models.Avg('tempo_processamento'))['tempo_processamento__avg'], 2)).zfill(2)
        extra_context['total_usuarios'] = str(Usuario.objects.count()).zfill(2)
        idioma_mais_comum = TextoDigitalizado.objects.values('idioma').annotate(total=Count('idioma')).order_by('-total').first()
        if idioma_mais_comum:
            extra_context['idioma_mais_comum'] = idioma_mais_comum['idioma']
            extra_context['idioma_mais_comum_count'] = str(idioma_mais_comum['total']).zfill(2)
        else:
            extra_context['idioma_mais_comum'] = "N/A"
            extra_context['idioma_mais_comum_count'] = '00'
            
        return super().index(request, extra_context)

admin.site = CustomAdminSite()
admin.site.register(Usuario)



