# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import models 
from django.db import models
from django.contrib.auth.models import User, Group
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
    usuario = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        usuario_salvo = None
        try:
            usuario_salvo = Pessoa.objects.get(email=self.email)
        except:
            print("erro")

        if usuario_salvo is None:
            usr = User(username=self.email)
            usr.set_password(self.senha)
            usr.save()
            self.usuario = usr
        super(Pessoa,self).save()

    def __str__(self):
        return self.nome
"""
Informações básicas das disciplinas envolvidas em um projeto determinado
"""
class Disciplinas(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=1000)

    def __str__(self):
        return self.nome
"""
Especifica o papel de professor para um usuário/pessoa, ao criar um professor, a nivel de usuário 
do sistemas são armazenadas as permissões de um professor
"""
class Professor(models.Model):
    pessoa = models.ForeignKey(Pessoa)

    def __str__(self):
        return self.pessoa.nome

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        pessoa_prof = None
        try:
            pessoa_prof = self.pessoa
        except:
            print("erro")

        if pessoa_prof is not None:
            grupo = Group.objects.get(name="Professores")
            grupo.user_set.add(pessoa_prof.usuario)
        super(Professor,self).save()

    def __str__(self):
        return self.pessoa.nome
"""
Especifica o papel de avaliador para um usuário/pessoa, ao criar um avaliador, a nivel de usuário
do sistema sao armazenadas as permissoes de um avaliador
"""
class Avaliador(models.Model):
    pessoa = models.ForeignKey(Pessoa)

    def __str__(self):
        return self.pessoa.nome

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        pessoa_aval = None
        try:
            pessoa_aval = self.pessoa
        except:
            print("erro")

        if pessoa_aval is not None:
            grupo = Group.objects.get(name="Avaliadores")
            grupo.user_set.add(pessoa_aval.usuario)
        super(Avaliador,self).save()
"""
Especifica o papel de avaliador para um usuário/pessoa, ao criar um aluno, a nivel de usuário 
do sistema sao armazenadas as permissoes de um aluno
"""
class Aluno(models.Model):
    pessoa = models.ForeignKey(Pessoa)

    def __str__(self):
        return self.pessoa.nome


    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        pessoa_aluno = None
        try:
            pessoa_aluno = self.pessoa
        except:
            print("erro")

        if pessoa_aluno is not None:
            grupo = Group.objects.get(name="Professores")
            grupo.user_set.add(pessoa_aluno.usuario)
        super(Aluno,self).save()
'''
Dados de um projeto, deve ser criado por um professor
sua especificação será criado via CKEditor, a ser implementado
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

'''
nomeprojeto é o nome do projeto do grupo, nao
 confundir com o nome do projeto(tema)'''

class Grupo(models.Model):
    projeto = models.ForeignKey(Projeto)
    nome = models.CharField(max_length=100)
    descricaoprojeto = models.CharField(max_length=1000)
    nomeprojeto = models.CharField(max_length=1000)
    alunos = models.ManyToManyField(Aluno)

    def __str__(self):
        return self.nome
"""
Etapas ou entregas de um projeto. assim como no projeto, a especificação será via o editor de 
rich-text Ckeditor, a ser implementada.
"""
class Etapas(models.Model):
    projeto = models.ForeignKey(Projeto)
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=1000)
    entrega = models.DateField()
    especificacao = tinymce_models.HTMLField()

    def __str__(self):
        return self.nome

"""
Criterios de avaliação da apresentação e seu peso
"""
class Criterios(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=1000)
    peso = models.FloatField()

    def __str__(self):
        return self.nome

"""
Consideramos a apresentação como uma especificacao de uma etapa
"""
class Apresentacao(Etapas):
    criterios = models.ManyToManyField(Criterios)

class Avaliacao(models.Model):
    avaliador = models.ForeignKey(Avaliador)
    criterio = models.ForeignKey(Criterios)
    nota = models.FloatField()

    def __str__(self):
        return self.avaliador.pessoa.nome + ' - ' + self.criterio.nome

"""
Dados referentes a avaliação especifica de um membro do grupo, só haverá avaliaçãoAluno caso o avaliador
considere que o mesmo nao merece a nota definida em avaliaçãogrupo.
"""
class AvaliacaoAluno(Avaliacao):
    aluno = models.ForeignKey(Aluno)

    def __str__(self):
        return self.aluno.pessoa.nome

"""
Avaliaçaogrupo e a avaliação de um grupo especifico por um avaliador.
"""
class AvaliacaoGrupo(Avaliacao):
    grupo = models.ForeignKey(Grupo)

    def __str__(self):
        return self.grupo.nome

"""
É o resultado final de uma etapa, do ponto de vista de um alunno. apresenta a data de 
entrega para verificaçao de possiveis atrosos de entrega.
"""
class Entregas(models.Model):
    Etapa = models.ForeignKey(Etapas)
    dataEntrega = models.DateField()
    aluno = models.ForeignKey(Aluno)

    def __str__(self):
        return self.etapa.nome + ' - ' + self.dataEntrega


