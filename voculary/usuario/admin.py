from datetime import date, timedelta

from django.contrib import admin, messages
from django.db.models import Avg, Count
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import path, reverse

from gerenciamento_texto.models import DigitizedText
from .models import User


class UsuarioAdmin(admin.ModelAdmin):
    # Atributos da classe
    list_display = ('is_active', 'id', 'email', 'first_name', 'last_name', 'data_formatada')
    list_display_links = None
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('is_active', 'is_staff', 'is_admin')
    list_per_page = 6
    actions = ['editar_usuarios_selecionados', 'visualizar_usuarios_selecionados']

    # Métodos padrão do admin
    def has_add_permission(self, request):
        """Verifica se o usuário tem permissão para adicionar."""
        return request.user.is_admin

    def has_change_permission(self, request, obj=None):
        """Verifica se o usuário tem permissão para alterar."""
        return request.user.is_admin

    def has_delete_permission(self, request, obj=None):
        """Verifica se o usuário tem permissão para deletar."""
        return request.user.is_admin

    def get_fieldsets(self, request, obj=None):
        """
        Sobrescreve campos do Admin.
        """
        fieldsets = super().get_fieldsets(request, obj)
        if obj:
            for fieldset in fieldsets:
                fields = list(fieldset[1]['fields'])
                if 'password' in fields:
                    fields.remove('password')
                    fieldset[1]['fields'] = tuple(fields)
                    break
        return fieldsets

    def get_actions(self, request):
        """Define as ações disponíveis de acordo com as permissões do usuário."""
        actions = super().get_actions(request)
        if not request.user.is_admin:
            actions.pop('editar_usuarios_selecionados', None)
        return actions

    # Métodos personalizados para ações no admin
    def editar_usuarios_selecionados(self, request, queryset):
        """Edita os usuários selecionados."""
        if queryset.count() == 1:
            user_id = queryset.first().id
            return HttpResponseRedirect(str(user_id))
        self.message_user(request, "Por favor, selecione apenas um usuário para editar.", level=messages.ERROR)

    def visualizar_usuarios_selecionados(self, request, queryset):
        """Visualiza os usuários selecionados."""
        if queryset.count() != 1:
            self.message_user(request, "Por favor, selecione apenas um usuário para visualizar.", level=messages.ERROR)
            return
        user_id = queryset.first().id
        return HttpResponseRedirect(reverse('admin:usuario_user_view', args=[user_id]))

    def delete_model(self, request, obj):
        """
        Sobrescreve o comportamento padrão da exclusão para desativar o usuário em vez de excluir.
        """
        obj.is_active = False
        obj.save()

    def delete_queryset(self, request, queryset):
        """
        Sobrescreve o comportamento padrão da exclusão em massa para desativar os usuários em vez de excluir.
        """
        queryset.update(is_active=False)
        messages.success(request, "Usuário(s) desativado(s) com sucesso!")

    def response_change(self, request, obj):
        """Customiza a resposta após uma mudança."""
        if "_deactivate" in request.POST:
            self.message_user(request, "Usuário(s) desativado(s) com sucesso.", level=messages.SUCCESS)
            return HttpResponseRedirect(reverse('admin:index'))
        return super().response_change(request, obj)

    # Métodos relacionados à visualização
    def data_formatada(self, obj):
        """Formata a data de registro do usuário."""
        return obj.date_joined.strftime('%d/%m/%Y')

    def get_urls(self):
        """Obtém as URLs customizadas para o admin."""
        urls = super().get_urls()
        custom_urls = [
            path('<int:user_id>/view/', self.admin_site.admin_view(self.visualizarUsuarioView), name='usuario_user_view'),
        ]
        return custom_urls + urls

    def visualizarUsuarioView(self, request, user_id, *args, **kwargs):
        """Renderiza a visualização de um usuário."""
        usuario = get_object_or_404(User)

class AdminSitePersonalizado(admin.AdminSite):
    # Atributo da classe
    site_header = "Painel do Administrador"

    # Métodos
    def index(self, request, extra_context=None):
        """Método que exibe a página inicial do painel de administração personalizado."""
        context = extra_context or {}

        # Estatísticas dos usuários
        total_usuarios = User.objects.count()
        total_usuarios_ativos = User.objects.filter(is_active=True).count()
        
        # Calcula o início e o final deste mês
        inicio_mes = date.today().replace(day=1)
        if date.today().month != 12:
            final_mes = date.today().replace(month=date.today().month + 1, day=1) - timedelta(days=1)
        else:
            final_mes = date(date.today().year, 12, 31)
        
        usuarios_mes = User.objects.filter(date_joined__range=(inicio_mes, final_mes)).count()

        # Calcula o início e o final desta semana
        inicio_semana = date.today() - timedelta(days=date.today().weekday())
        final_semana = inicio_semana + timedelta(days=6)
        usuarios_semana = User.objects.filter(date_joined__range=(inicio_semana, final_semana)).count()

        # Estatísticas dos textos
        total_textos = DigitizedText.objects.count()
        tempo_medio_processamento = round(DigitizedText.objects.aggregate(Avg('processing_time'))['processing_time__avg'], 2)

        # Idioma mais comum entre os textos
        idioma_mais_comum = DigitizedText.objects.values('language').annotate(total=Count('language')).order_by('-total').first()
        idioma = idioma_mais_comum['language'] if idioma_mais_comum else "N/A"
        total_idioma = str(idioma_mais_comum['total']).zfill(2) if idioma_mais_comum else '00'

        # Atualização do contexto
        context.update({
            'total_textos': str(total_textos).zfill(2),
            'tempo_medio_processamento': str(tempo_medio_processamento).zfill(2),
            'total_usuarios_ativos': str(total_usuarios_ativos).zfill(2),
            'usuarios_mes': str(usuarios_mes).zfill(2),
            'usuarios_semana': str(usuarios_semana).zfill(2),
            'idioma_mais_comum': idioma,
            'idioma_mais_comum_count': total_idioma
        })
            
        return super().index(request, context)

# Instancia e registra o site de administração personalizado
admin_site = AdminSitePersonalizado(name='admin_site')
admin_site.register(User, UsuarioAdmin)