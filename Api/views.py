# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.views import APIView
from django.shortcuts import render
from django.contrib.auth import authenticate,login
from rest_framework.response import Response
from rest_framework import status
from serializers import ProjetosSerializer, GrupoSerializer,AlunosSerializer,CriteriosSerializer
from serializers import AvaliacaoGrupoSerializer,AvaliacaoAlunoSerializer
from models import Projeto,Grupo,Aluno,Criterios,Apresentacao

class Login(APIView):
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

class ProjetosView(APIView):
    def get(self,request):
        projetos = Projeto.objects.filter(ativo=True)
        serializer = ProjetosSerializer(projetos,many=True)
        if serializer.is_valid():
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self,request):
        if request.data['id'] is not None:
            id = int(request.data['id'])
            projeto = Projeto.objects.get(pk=id)
            if projeto is not None:
                serializer = ProjetosSerializer(projeto)
                return Response(serializer.data)
            else:
                message = {'message':'Busca invalida'}
                return Response(message,status=status.HTTP_400_BAD_REQUEST)
        else:
            message = {'message':'Os dados nao foram enviados'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

class GruposView(APIView):
    def get(self,request):
        if request.data['id'] is not None:
            id = int(request.data['id'])
            grupo = Grupo.objects.filter(pk=id)
            if grupo is not None:
                serializer = GrupoSerializer(grupo)
                return Response(serializer.data)
            else:
                message = {'message':'Grupo nao encontrado'}
                return Response(message,status=status.HTTP_400_BAD_REQUEST)

        elif request.data['projeto'] is not None:
            id = int(request.data['projeto'])
            grupos = Grupo.objects.filter(projeto=id)
            if grupos is not None:
                serializer = GrupoSerializer(grupos,many=True)
                return Response(serializer.data)
            else:
                message = {'message': 'Grupo nao encontrado'}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)

        else:
            message = {'message': 'Busca invalida'}
            return Response(message,status=status.HTTP_400_BAD_REQUEST)

    def post(self,request):
        pass


class AlunosView(APIView):

    def get(self,request):
        if request.data['id'] is not None:
            id = int(request.data['id'])
            aluno = Aluno.objects.get(pk=id)
            if aluno is not None:
                serializer = AlunosSerializer(aluno)
                return Response(serializer.data)
            else:
                message = {'message':'Aluno nao encontrado'}
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            message = {'message':'Busca invalida'}
            return Response(message,status=status.HTTP_400_BAD_REQUEST)
    def post(self,request):
        pass

class CriteriosView(APIView):

    def get(self,request):
        if request.data['projeto'] is not None:
            idprojeto = request.data['projeto']
            apresentacao = Apresentacao.objects.filter(projeto=idprojeto)
            if apresentacao is not None:
                criterios = Apresentacao.criterios
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
    def get(self,request):
        return Response(status=status.HTTP_200_OK)
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
    def get(self,request):
        return Response(status=status.HTTP_200_OK)
    def post(self,request):
        serializer = AvaliacaoAlunoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            message = {'message':'Salvo'}
            return Response(message,status=status.HTTP_201_CREATED)
        else:
            message = {'message': 'dados invalidos'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)