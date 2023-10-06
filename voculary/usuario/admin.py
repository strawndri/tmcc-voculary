from django.contrib import admin
from .models import User
from gerenciamento_texto.models import DigitizedText
from django.db.models import Count, Avg

class UserAdmin(admin.ModelAdmin):
    list_display = ('is_active', 'id', 'first_name', 'last_name', 'email', 'date_registered')
    list_display_links = None
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('is_active', 'is_staff', 'is_admin')
    list_editable = ('is_active',)
    list_per_page = 10

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
