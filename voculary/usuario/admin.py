from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Count, Avg
from .models import User
from gerenciamento_texto.models import DigitizedText

from datetime import date, timedelta

class UsuarioAdmin(admin.ModelAdmin):
    def data_formatada(self, obj):
        return obj.date_registered.strftime('%d/%m/%Y')
    data_formatada.admin_order_field = 'date_registered'
    data_formatada.short_description = 'Data de registro'

    def editar_usuarios_selecionados(self, request, queryset):
        if queryset.count() == 1:
            user_id = queryset.first().id
            return HttpResponseRedirect(str(user_id))
        self.message_user(request, "Por favor, selecione apenas um usuário para editar.", level=messages.ERROR)

    def response_change(self, request, obj):
        if "_deactivate" in request.POST:
            obj.is_active = False
            obj.save()
            self.message_user(request, "Usuário foi desativado com sucesso.", level=messages.SUCCESS)
            return HttpResponseRedirect(reverse('admin:index'))
        return super().response_change(request, obj)

    list_display = ('is_active', 'id', 'email', 'first_name', 'last_name', 'data_formatada')
    list_display_links = None
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('is_active', 'is_staff', 'is_admin')
    list_editable = ('is_active',)
    list_per_page = 6

    editar_usuarios_selecionados.short_description = "Editar usuário selecionado"
    actions = [editar_usuarios_selecionados]

class AdminSitePersonalizado(admin.AdminSite):
    site_header = "Painel do Administrador"

    def index(self, request, extra_context=None):
        context = extra_context or {}

        # Total de usuários ativos
        total_usuarios_ativos = User.objects.filter(is_active=True).count()

        # Usuários que ingressaram neste mês
        inicio_mes = date.today().replace(day=1)
        usuarios_mes = User.objects.filter(date_registered=inicio_mes).count()

        # Usuários que ingressaram nesta semana
        inicio_semana = date.today() - timedelta(days=date.today().weekday())
        usuarios_semana = User.objects.filter(date_registered=inicio_semana).count()

        context.update({
            'total_textos': str(DigitizedText.objects.count()).zfill(2),
            'tempo_medio_processamento': str(round(DigitizedText.objects.aggregate(Avg('processing_time'))['processing_time__avg'], 2 )).zfill(2),
            'total_usuarios_ativos': str(total_usuarios_ativos).zfill(2),
            'usuarios_mes': str(usuarios_mes).zfill(2),
            'usuarios_semana': str(usuarios_semana).zfill(2),
        })

        idioma_mais_comum = DigitizedText.objects.values('language').annotate(total=Count('language')).order_by('-total').first()

        context['idioma_mais_comum'] = idioma_mais_comum['language'] if idioma_mais_comum else "N/A"
        context['idioma_mais_comum_count'] = str(idioma_mais_comum['total']).zfill(2) if idioma_mais_comum else '00'
            
        return super().index(request, context)

admin_site = AdminSitePersonalizado(name='admin_site')
admin_site.register(User, UsuarioAdmin)
