#encoding=utf-8
from django.db import models

# Create your models here.
class Medico(models.Model):
    nome = models.CharField(max_length=64)
    tratamento = models.CharField(max_length=16)
    email = models.EmailField(unique=True)
    crm = models.Charfield(max_length=32, unique=True)
    endereco = models.ForeignKey(Endereco)


class Endereco(models.Model):
    #Rua*
    #cep*
    #pais*
    #estado*
    #cidade*
    pass

class Paciente(models.Model):
    #nome
    #creim*
    pass
class Amostra(models.Model):
    #tipo
    #data_recebimento
    #data_autorizacao
    pass

class Laudo(models.Model):
    #paciente
    #medico
    #amostra
    #data
    #metodologia(texto)
    #resultado(lista de mutacoes) -->
    #interpretacao(texto)
    #referencias -->
    pass

class Referencia(models.Model):
    #Autores
    #titulo
    #link
    #jornal
    pass

class Doenca(models.Model):
    #nome
    #descricao
    #genes -->
    pass

class Genes(models.Model):
    #simbolo
    #refseq
    #cromossomo
    pass

class VariantesGenicas(models.Model):
    #codigo_nt
    #codigo_prot
    #gene -->
    #localizacao
    #patogenicidade(choicefield)
    #referencias -->
    pass
