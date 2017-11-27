# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.views import APIView
from django.shortcuts import render
from django.contrib.auth import authenticate,login
from rest_framework.response import Response
from rest_framework import status
from serializers import ProjetosSerializer, GrupoSerializer,AlunosSerializer,CriteriosSerializer
from serializers import AvaliacaoGrupoSerializer,AvaliacaoAlunoSerializer, PessoaSerializer
from models import Projeto,Grupo,Aluno,Criterios,Apresentacao,AvaliacaoGrupo,AvaliacaoAluno, Pessoa
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from itertools import chain

#filé
class Login(APIView):
    """
    Em desuso, as restrições de acesso são realizadas via token JWT, a ser enviado pelo cliente e criado
    em http://127.0.0.1:8000/api/token
    post:
    recebe via post email e senha de um usuáario cadastrado e realiza a autenticação
    """
    def get(self,request):
        return Response(status=status.HTTP_200_OK)

    def post(self,request):
        usuario = authenticate(username=request.data['email'], password=request.data['senha'])
        if usuario is not None:
            if usuario.is_active:
                login(request, usuario)
                dadosusuario = {"usuario": unicode(request.user)}
                return Response(dadosusuario, status=status.HTTP_201_CREATED)
        else:
            dados = {'Login nao efetuado': 'Usuario ou senha incorretos'}
            return Response(dados, status=status.HTTP_401_UNAUTHORIZED)
#show de bola
class ProjetosView(APIView):
    """
    get:
        envia todos os projetos cadastrados.
    post:
        envia dados de um projeto especifico, é necessario o envio de um id via post
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)
    def get(self,request,proj=None,format=None):

        if proj is not None:
            proj_query = Projeto.objects.get(pk=proj)
            serializer = ProjetosSerializer(proj_query, many=False)
            return Response(serializer.data)
        else:
            projetos = Projeto.objects.filter(ativo=True)
            if projetos.exists():
                serializer = ProjetosSerializer(projetos,many=True)
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self,request):
        """if request.data['id'] is not None:
            id = int(request.data['id'])
            try:
                projeto = Projeto.objects.get(pk=id)
            except:
                projeto = None
            if projeto is not None:  #exists() nao funciona is not None tambem nao
                serializer = ProjetosSerializer(projeto)
                return Response(serializer.data)
            else:
                message = {'message':'Busca invalida'}
                return Response(message,status=status.HTTP_400_BAD_REQUEST)
        else:
            message = {'message':'Os dados nao foram enviados'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)"""
        pass
#muito bom
class ProjetosGruposView(APIView):
    def get(self,request,proj=None):
        if proj is not None:
            try:
                grupos = Grupo.objects.filter(projeto=proj)
            except:
                grupos = None
            if grupos is not None:
                serializer = GrupoSerializer(grupos,many=True)
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self,request):
        pass
#bom demais
class GruposView(APIView):
    """
    Envia as informações dos grupos
    get:
        envia as informações do grupo especifico enviando o parametro id ou dos grupos de um projeto
        enviando o parametro projeto.
    """
    #permission_classes = (IsAuthenticated,)
    #authentication_classes = (JSONWebTokenAuthentication,)

    def get(self,request,grpo=None):
        if grpo is not None:
            try:
                grupo_desejado = Grupo.objects.get(pk=grpo)
            except:
                grupo_desejado = None
            if grupo_desejado is not None:
                serializer = GrupoSerializer(grupo_desejado,many=False)
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            grupo_all = Grupo.objects.all()
            serializer = GrupoSerializer(grupo_all, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self,request):
        pass
#show de bola
class AlunosView(APIView):


    """
    Retorna dados dos alunos
    get:
        ao receber o parametro id, retorna as informações cadastradas daquele aluno.
    """

    #permission_classes = (IsAuthenticated,)
    #authentication_classes = (JSONWebTokenAuthentication,)
    def get(self,request,aln=None):
        if aln is not None:
            try:
                aluno = Aluno.objects.get(pk=aln)
            except:
                aluno = None
            if aluno is not None:
                serializer = PessoaSerializer(aluno.pessoa,many=False)
                return Response(serializer.data)
            else:
                message = {'message':'Aluno nao encontrado'}
                return Response(message,status=status.HTTP_400_BAD_REQUEST)
        else:
            all_alunos = Aluno.objects.all()
            pessoa_list = list()
            for aluno in all_alunos:
                pessoa_list.append(aluno.pessoa)
            qs_vazio = Pessoa.objects.none()
            qs = list(chain(qs_vazio,pessoa_list))
            serializer = PessoaSerializer(qs,many=True)
            return Response(serializer.data)
    def post(self,request):
        pass
#muito legal
class CriteriosView(APIView):
    """
    Retorna os criterios de avaliação de um determinado projeto
    get:
        ao receber o parametro projeto os criterios vinculados aquele projeto sao enviados.
    """

    #permission_classes = (IsAuthenticated,)
    #authentication_classes = (JSONWebTokenAuthentication,)


    def get(self,request,projeto=None):
        if projeto is not None:
            apresentacao = Apresentacao.objects.get(projeto=projeto)
            ##SUPONDO APENAS UMA APRESENTAÇÃO POR PROJETO
            ##CASO HAJA MAIS DE UMA, ALTERAR O ATRIBUTO GET PARA O ID DA APRESENTAÇÃO E CRIAR METODO
            ##PARA BUSCAR APRESENTAÇÕES POR PROJETO.
            if apresentacao is not None:
                criterios = apresentacao.criterios
                serializer = CriteriosSerializer(criterios,many=True)
                return Response(serializer.data)
            else:
                message = {'message':'não encontrado'}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
        else:
            message = {'message': 'não encontrado'}
            return Response(message,status=status.HTTP_400_BAD_REQUEST)
    def post(self,request):
        pass

class AvaliacaoGrupoView(APIView):
    """
    Lida com os dados das avaliações de grupo
    get:
        envia as avaliaçoes cadastradas
    post:
        recebe os dados (avaliador,criterio,nota,grupo) de uma avalicao os serializa e cadastra no sistema

    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get(self,request):
        avaliacoes = AvaliacaoGrupo.objects.all()
        serializer = AvaliacaoGrupoSerializer(avaliacoes,many=True)
        return Response(serializer.data)
    def post(self,request):
        serializer = AvaliacaoGrupoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            message = {'message':'Salvo'}
            return Response(message,status=status.HTTP_201_CREATED)
        else:
            message = {'message': 'dados invalidos'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

class AvaliacaoAlunoView(APIView):
    """
    Lida com os dados das avaliações de grupo
    get:
        envia as avaliaçoes cadastradas
    post:
        recebe os dados (avaliador,criterio,nota,aluno) de uma avalicao os serializa e cadastra no sistema

    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get(self,request):
        avaliacoes = AvaliacaoAluno.objects.all()
        serializer = AvaliacaoAlunoSerializer(avaliacoes, many=True)
        return Response(serializer.data)
    def post(self,request):
        serializer = AvaliacaoAlunoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            message = {'message':'Salvo'}
            return Response(message,status=status.HTTP_201_CREATED)
        else:
            message = {'message': 'dados invalidos'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
#muito show
class GrupoAlunosView(APIView):
    def get(self,request,grpo=None):
        if grpo is not None:
            alunos_grupo = Grupo.objects.get(pk=grpo).alunos
            serializer = AlunosSerializer(alunos_grupo,many=True)
            return Response(serializer.data)
    def post(self,request):
        pass