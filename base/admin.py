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
            )

class EnderecoAdminInline(GenericStackedInline):
    model = Endereco
    verbose_name = _(u'endereço')
    verbose_name_plural = _(u'endereços')

class MedicoAdmin(admin.ModelAdmin):
    inlines = (EnderecoAdminInline,)

admin.site.register(Medico, MedicoAdmin)
