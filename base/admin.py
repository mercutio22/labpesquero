#encoding=utf-8
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.generic import GenericStackedInline

from .models import (
            Medico,
            Endereco,
            Paciente,
            Amostra,
            Gene,
            VarianteGenica,
            Laudo,
            Doenca,
            Metodologia,
            VariantePaciente,
            DosagemAEnzimatica,
            )

class DosagemAEnzimaticaAdmin(admin.ModelAdmin):
    model = DosagemAEnzimatica
    raw_id_fields = ('gene', 'paciente')
    autocomplete_lookup_fields = { 'fk': ['gene', 'paciente']}

class DoencaAdmin(admin.ModelAdmin):
    search_fields = ['nome', 'descricao',]
    #raw_id_fields = ('genes',)
    #autocomplete_lookup_fields = {
    #    'm2m': ['genes'],
    #}
    filter_horizontal = ('genes',)

class EnderecoAdminInline(GenericStackedInline):
    model = Endereco
    verbose_name = _(u'endereço')
    verbose_name_plural = _(u'endereços')
    max_num = 2

class MedicoAdmin(admin.ModelAdmin):
    inlines = (EnderecoAdminInline,)
    search_fields = ['nome', 'crm']

class VariantePacienteInline(admin.StackedInline):
    model = VariantePaciente
    autocomplete_lookup_fields = {
        'fk': ['variante', 'paciente'] 
    }

class VariantePacienteAdmin(admin.ModelAdmin):
    model = VariantePaciente
    search_fields = [
            'codigo_nt', 
            'codigo_prot', 
            'paciente__nome', 
            'paciente__sigla']
    list_display = ['variante', 'paciente', 'zigosidade']

class PacienteAdmin(admin.ModelAdmin):
    inlines = (EnderecoAdminInline,)
    readonly_fields = ('id',)
    search_fields = ['nome', 'id']

class AmostraAdmin(admin.ModelAdmin):
    raw_id_fields = ('paciente',)
    search_fields = ['paciente__nome', 'creim', 'data_recebimento',]
    list_display = ['paciente', 'creim'] 

class GeneAdmin(admin.ModelAdmin):
    search_fields = ['simbolo',]

class VarianteGenicaAdmin(admin.ModelAdmin):
    list_display = ('localizacao','codigo_nt', 'codigo_prot', 'gene',
            'patogenicidade',)
    search_fields = ['codigo_nt', 'codigo_prot','gene__simbolo',
        'patogenicidade',
    ]
    raw_id_fields = ('gene',)
    filter_horizontal = ['referencias','doenca']
    autocomplete_lookup_fields = { 'fk': ['gene']}
    list_display_links = ['codigo_nt', 'codigo_prot']

class LaudoAdmin(admin.ModelAdmin):
    search_fields = ['paciente__nome','medico__nome', 'metodologia', 
        'interpretacao',
    ]
    raw_id_fields = ('paciente', 'medico', 'amostra')
    list_display = ['paciente','medico', 'amostra', 'data', 'cobrado']
    list_display_links = ['paciente', 'data',]
    list_filter = ('data',)
    filter_horizontal = ('variantes',)
    autocomplete_lookup_fields = {
        'fk': ['paciente', 'medico', 'amostra'],
    #    'm2m': ['variantes']
    }

class MetodologiaAdmin(admin.ModelAdmin):
    search_fields=('sigla', 'descricao')

admin.site.register(Medico, MedicoAdmin)
admin.site.register(Paciente, PacienteAdmin)
admin.site.register(Amostra, AmostraAdmin)
admin.site.register(Gene, GeneAdmin)
admin.site.register(VarianteGenica, VarianteGenicaAdmin)
admin.site.register(Laudo, LaudoAdmin)
admin.site.register(Doenca, DoencaAdmin)
admin.site.register(Metodologia, MetodologiaAdmin)
admin.site.register(VariantePaciente, VariantePacienteAdmin)
