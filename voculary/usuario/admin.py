from django.contrib import admin
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import User
from gerenciamento_texto.models import DigitizedText
from django.db.models import Count, Avg
from django.urls import reverse

class UserAdmin(admin.ModelAdmin):
    def formatar_data(self, obj):
        return obj.date_registered.strftime('%d/%m/%Y')

    def edit_selected_users(modeladmin, request, queryset):
        if queryset.count() == 1:
            user_id = queryset.first().id
            url = f"{user_id}"
            return HttpResponseRedirect(url)
        else:
            modeladmin.message_user(request, "Por favor, selecione apenas um usuário para editar.", level=messages.ERROR)

    def response_change(self, request, obj):
        if "_deactivate" in request.POST:
            obj.is_active = False
            obj.save()
            self.message_user(request, "Usuário foi desativado com sucesso.", level=messages.SUCCESS)
            return HttpResponseRedirect(reverse('admin:index'))
        return super().response_change(request, obj)
    
    formatar_data.admin_order_field = 'date_registered'
    formatar_data.short_description = 'Data de registro'

    list_display = ('is_active', 'id', 'email', 'first_name', 'last_name', 'formatar_data')
    list_display_links = None
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('is_active', 'is_staff', 'is_admin')
    list_editable = ('is_active',)
    list_per_page = 6

    edit_selected_users.short_description = "Editar usuário selecionado"

    actions = [edit_selected_users]

class MyAdminSite(admin.AdminSite):
    site_header = "Painel do Administrador"

    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['total_textos'] = str(DigitizedText.objects.count()).zfill(2)
        extra_context['tempo_medio_processamento'] = str(round(DigitizedText.objects.aggregate(Avg('processing_time'))['processing_time__avg'], 2)).zfill(2)
        extra_context['total_usuarios'] = str(User.objects.count()).zfill(2)
        
        most_common_language = DigitizedText.objects.values('language').annotate(total=Count('language')).order_by('-total').first()
        
        if most_common_language:
            extra_context['idioma_mais_comum'] = most_common_language['language']
            extra_context['idioma_mais_comum_count'] = str(most_common_language['total']).zfill(2)
        else:
            extra_context['idioma_mais_comum'] = "N/A"
            extra_context['idioma_mais_comum_count'] = '00'
            
        return super().index(request, extra_context)

admin_site = MyAdminSite(name='admin_site')
admin_site.register(User, UserAdmin)
