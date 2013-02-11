#encoding=utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from publications.models.publication import Publication


class Endereco(models.Model):
    Rua = models.CharField(max_length=64)
    cep = models.CharField(max_length=13)
    pais = models.CharField(max_length=64)
    estado = models.CharField(max_length=2)
    cidade = models.CharField(max_length=64)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()

class Pessoa(models.Model):
    nome = models.CharField(max_length=64)
    email = models.EmailField(unique=True)
    endereco = generic.GenericRelation(Endereco)

    class Meta:
        abstract = True

class Medico(Pessoa):
    tratamento = models.CharField(max_length=16)
    crm = models.CharField(max_length=32, unique=True)


class Paciente(Pessoa):
    sigla = models.CharField(max_length=32)

class Amostra(models.Model):

    TIPO_CHOICES = (
        ('ST', _('Sangue em tubo com EDTA')),
        ('FTA', _('Sangue em FTA')),
        ('SPF', _('Sangue em papel filtro')),
        ('eDNA', _('DNA extraído')),
    )
    creim = models.PositiveIntegerField()
    tipo = models.CharField(max_length=4, choices=TIPO_CHOICES)
    data_recebimento = models.DateField()
    data_autorizacao = models.DateField()
    paciente = models.ForeignKey(Paciente)

class Laudo(models.Model):
    paciente = models.ForeignKey(Paciente)
    medico = models.ForeignKey(Medico)
    amostra = models.ForeignKey(Amostra)
    data = models.DateField()
    metodologia = models.TextField()
    #resultado(lista de mutacoes) -->
    interpretacao = models.TextField()
    referencias = models.ManyToManyField(Publication)


class Doenca(models.Model):
    nome = models.CharField(max_length='64')
    descricao = models.TextField()
    genes = models.ManyToManyField('Gene')

class Gene(models.Model):
    simbolo = models.CharField(max_length=128)
    description = models.TextField(max_length=765)

class VarianteGenica(models.Model):
    VCHOICES = (
        ('p', _(u'variante patogênica')),
        ('c', _(u'variante comum')),
        ('d', _(u'variante de efeito desconhecido')),
    )
    codigo_nt = models.CharField(max_length=128)
    codigo_prot = models.CharField(max_length=128)
    gene = models.ForeignKey(Gene)
    patogenicidade = models.CharField(max_length=4, choices=VCHOICES)
    referencias = models.ManyToManyField(Publication)
