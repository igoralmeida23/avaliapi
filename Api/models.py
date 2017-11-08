# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import models
from django.db import models
from django.contrib.auth.models import User
from tinymce import models as tinymce_models

"""
Usuario e senha armazenados apenas na criação, onde será criado um usuario django e 
a senha será apagada por questoes de segurança
"""
class Pessoa(models.Model):
    nome =  models.CharField(max_length=100,unique=False)
    email = models.EmailField(max_length=100)
    telefone = models.CharField(max_length=11)
    senha= models.CharField(max_length=50)
    usuario = models.ForeignKey(User)

    def __str__(self):
        return self.nome


class Disciplinas(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=1000)

    def __str__(self):
        return self.nome


class Professor(models.Model):
    pessoa = models.ForeignKey(Pessoa)

    def __str__(self):
        return self.pessoa.nome


class Avaliador(models.Model):
    pessoa = models.ForeignKey(Pessoa)

    def __str__(self):
        return self.pessoa.nome


class Aluno(models.Model):
    pessoa = models.ForeignKey(Pessoa)

    def __str__(self):
        return self.pessoa.nome


'''
ativo diz respeito a se o projeto está para ser avaliado ou se ja encontra finalizado
tinymce é um editor de rich text suportado pelo django
'''
class Projeto(models.Model):
    tema = models.CharField(max_length=100)
    professor = models.ForeignKey(Professor)
    especificacao = tinymce_models.HTMLField()
    descricao = models.CharField(max_length=1000)
    ativo = models.BooleanField()
    disciplinas = models.ManyToManyField(Disciplinas)

    def __str__(self):
        return self.tema

'''nomeprojeto é o nome do projeto do grupo, nao confundir com o nome do projeto(tema)'''

class Grupo(models.Model):
    projeto = models.ForeignKey(Projeto)
    nome = models.CharField(max_length=100)
    descricaoprojeto = models.CharField(max_length=1000)
    nomeprojeto = models.CharField(max_length=1000)
    alunos = models.ManyToManyField(Aluno)

    def __str__(self):
        return self.nome


class Etapas(models.Model):
    projeto = models.ForeignKey(Projeto)
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=1000)
    entrega = models.DateField()
    especificacao = tinymce_models.HTMLField()

    def __str__(self):
        return self.nome


class Criterios(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=1000)
    peso = models.FloatField()

    def __str__(self):
        return self.nome


class Apresentacao(Etapas):
    criterios = models.ManyToManyField(Criterios)

class Avaliacao(models.Model):
    avaliador = models.ForeignKey(Avaliador)
    criterio = models.ForeignKey(Criterios)
    nota = models.FloatField()

    def __str__(self):
        return self.avaliador.pessoa.nome + ' - ' + self.criterio.nome


class AvaliacaoAluno(Avaliacao):
    aluno = models.ForeignKey(Aluno)

    def __str__(self):
        return self.aluno.pessoa.nome


class AvaliacaoGrupo(Avaliacao):
    grupo = models.ForeignKey(Grupo)

    def __str__(self):
        return self.grupo.nome


class Entregas(models.Model):
    Etapa = models.ForeignKey(Etapas)
    dataEntrega = models.DateField()
    aluno = models.ForeignKey(Aluno)

    def __str__(self):
        return self.etapa.nome + ' - ' + self.dataEntrega


