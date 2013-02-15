# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.core.urlresolvers import reverse

from publications.models.publication import Publication

              

class Endereco(models.Model):
    TIPO_CHOICES = ( 
            (0, _(u'comercial')),
            (1, _(u'residencial')),
    )
    tipo = models.PositiveIntegerField(choices=TIPO_CHOICES)
    logradouro = models.CharField(verbose_name=_(u'logradouro'), max_length=64)
    cep = models.CharField(max_length=13)
    pais = models.CharField(max_length=64, verbose_name=_(u'país'))
    estado = models.CharField(max_length=2)
    cidade = models.CharField(max_length=64)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()

    def __unicode__(self):
        return '{}: {} - {}'.format(self.tipo, self.cidade, self.logradouro)

class Pessoa(models.Model):
    """Classe abstrata com atributos comuns a Medico e Paciente """
    nome = models.CharField(max_length=64, blank=True)
    email = models.EmailField(unique=True, blank=True)
    endereco = generic.GenericRelation(Endereco)

    class Meta:
        abstract = True

class Medico(Pessoa):
    tratamento = models.CharField(max_length=16, blank=True)
    crm = models.CharField(max_length=32, unique=True,
            verbose_name=u'CRM', blank=True)
    
    @staticmethod
    def autocomplete_search_fields():
        """ method required for grappelli autocomplete searches"""
        return ("id__iexact", "nome__icontains",)

    def __unicode__(self):
        return '{} {}'.format(self.tratamento, self.nome)


class Paciente(Pessoa):
    sigla = models.CharField(max_length=32, blank=True)

    @staticmethod
    def autocomplete_search_fields():
        return ("id__iexact", "nome__icontains",)

    def __unicode__(self):
        return '{}: {}'.format(self.sigla, self.nome)

class Amostra(models.Model):

    TIPO_CHOICES = (
        ('ST', _(u'Sangue em tubo com EDTA')),
        ('FTA', _(u'Sangue em FTA')),
        ('SPF', _(u'Sangue em papel filtro')),
        ('eDNA', _(u'DNA extraído')),
    )
    creim = models.PositiveIntegerField()
    tipo = models.CharField(max_length=4, choices=TIPO_CHOICES)
    data_recebimento = models.DateField()
    data_autorizacao = models.DateField()
    paciente = models.ForeignKey(Paciente)

    @staticmethod
    def autocomplete_search_fields():
        return ("id__iexact", "creim__icontains",)

    def __unicode__(self):
        return '{}: {}'.format(self.creim, self.tipo)

class Metodologia(models.Model):
    sigla = models.CharField(max_length=32)
    descricao = models.TextField(max_length=800)

    def __unicode__(self):
        return str(self.sigla)

class Doenca(models.Model):
    nome = models.CharField(max_length='64')
    descricao = models.TextField(blank=True)
    genes = models.ManyToManyField('Gene', blank=True)
    
    class Meta:
        verbose_name = _(u'doença')

    def __unicode__(self):
        return str(self.nome)

class Gene(models.Model):
    simbolo = models.CharField(max_length=128)
    description = models.TextField(max_length=765, blank=True)
    
    @staticmethod
    def autocomplete_search_fields(self):
        return ('id__iexact', 'simbolo__icontains', 'description__icontains',)
    
    def __unicode__(self):
        return str(self.simbolo)

class VarianteGenica(models.Model):
    """Representa uma veriante descrita na literatura"""

    VCHOICES = (
        ('p', _(u'variante patogênica')),
        ('c', _(u'variante comum')),
        ('d', _(u'variante de efeito desconhecido')),
    )
    codigo_nt = models.CharField(max_length=128, unique=True, blank=True)
    codigo_prot = models.CharField(max_length=128, blank=True)
    localizacao = models.CharField(max_length=32, 
        help_text=_(u'contexo genômico, i.e. intron2, exon4, entre genes, etc')
    )
    gene = models.ForeignKey(Gene, blank=True, null=True)
    patogenicidade = models.CharField(max_length=4, choices=VCHOICES)
    referencias = models.ManyToManyField(Publication, blank=True)
    doenca = models.ManyToManyField(Doenca, blank=True)    

    class Meta:
        verbose_name = _(u'variante gênica')
        verbose_name_plural = _(u'variantes gênicas')

    @staticmethod
    def autocomplete_search_fields():
        """ method required for grappelli autocomplete searches"""

        return ("id__iexact", "codigo_nt__icontains",'codigo_prot__icontains')

    def __unicode__(self):
        if self.codigo_nt: 
            return str(self.codigo_nt)
        else:
            return str(self.codigo_prot)

class VariantePaciente(models.Model):
    """Essa classe representa uma variente gênica presente em um paciente 
    específico.
    """

    ZIGOSIDADE_CHOICES = (
        (0, _(u'em homozigose')),
        (1, _(u'em hemizigose')),
        (2, _(u'em heterozigose')),
    )
    zigosidade = models.PositiveIntegerField(choices=ZIGOSIDADE_CHOICES)
    variante = models.ForeignKey(VarianteGenica)
    paciente = models.ForeignKey(Paciente) 
    
    class Meta:
        verbose_name = _(u'Variante do paciente')
        verbose_name_plural = _(u'Variantes do paciente')
    
    def __unicode__(self):
        if self.variante.codigo_nt:
            return '{}: {} -> {}'.format(self.variante.codigo_nt, 
                self.zigosidade, self.paciente.nome)
        else:
            return '{}: {} -> {}'.format(self.variante.codigo_prot, 
                self.zigosidade, self.paciente.nome)

class Laudo(models.Model):
    """ Instâncias desta classe contém todas as informações necessárias
     para gerar um laudo de um Paciente"""

    TIPO_LAUDO = (
        (1, _(u'triagem')),
        (2, _(u'índice')),
    )
    tipo = models.PositiveIntegerField(choices=TIPO_LAUDO)
    paciente = models.ForeignKey(Paciente)
    medico = models.ForeignKey(Medico)
    amostra = models.ForeignKey(Amostra)
    data = models.DateField()
    metodologia = models.ForeignKey(Metodologia)
    interpretacao = models.TextField()
    variantes = models.ManyToManyField(VariantePaciente)
    obs = models.TextField(max_length=800, 
        help_text=_(u'use este campo para informações adicionais')
    ) 

    def get_absolute_url(self):
        """Faz aparecer o link 'mostrar no site' na interface admin"""
        return reverse('laudo-detalhe', kwargs={ 'pk':str(self.id)})
   
    def __unicode__(self):
        return '{} - {}'.format(self.paciente, self.data)

