# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

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
    nome = models.CharField(max_length=64, blank=True)
    email = models.EmailField(unique=True, blank=True)
    endereco = generic.GenericRelation(Endereco)

    class Meta:
        abstract = True

class Medico(Pessoa):
    tratamento = models.CharField(max_length=16)
    crm = models.CharField(max_length=32, unique=True,
            verbose_name=u'CRM')
    
    def __unicode__(self):
        return '{} {}'.format(self.tratamento, self.nome)


class Paciente(Pessoa):
    sigla = models.CharField(max_length=32)

    def __unicode__(self):
        return 'Paciente {}: {}'.format(self.sigla, self.nome)

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

    def __unicode__(self):
        return '{}: {}'.format(self.creim, self.tipo)

class Metodologia(models.Model):
    sigla = models.CharField(max_length=32)
    descricao = models.TextField(max_length=800)

class Laudo(models.Model):
    paciente = models.ForeignKey(Paciente)
    medico = models.ForeignKey(Medico)
    amostra = models.ForeignKey(Amostra)
    data = models.DateField()
    metodologia = models.ForeignKey(Metodologia)
    #resultado(lista de mutacoes) -->
    interpretacao = models.TextField()

    def __unicode__(self):
        return '{} - {}'.format(self.paciente, self.data)


class Doenca(models.Model):
    nome = models.CharField(max_length='64')
    descricao = models.TextField()
    genes = models.ManyToManyField('Gene')
    
    class Meta:
        verbose_name = _(u'doença')

    def __unicode__(self):
        return str(self.nome)

class Gene(models.Model):
    simbolo = models.CharField(max_length=128)
    description = models.TextField(max_length=765)
    
    def __unicode__(self):
        return str(self.simbolo)

class VarianteGenica(models.Model):
    VCHOICES = (
        ('p', _(u'variante patogênica')),
        ('c', _(u'variante comum')),
        ('d', _(u'variante de efeito desconhecido')),
    )
    codigo_nt = models.CharField(max_length=128, blank=True)
    codigo_prot = models.CharField(max_length=128, blank=True)
    gene = models.ForeignKey(Gene)
    patogenicidade = models.CharField(max_length=4, choices=VCHOICES)
    referencias = models.ManyToManyField(Publication)
    
    class Meta:
        verbose_name = _(u'variante gênica')
        verbose_name_plural = _(u'variantes gênicas')

    def __unicode__(self):
        if self.codigo_nt: 
            return str(self.codigo_nt)
        else:
            return str(self.codigo_prot)
