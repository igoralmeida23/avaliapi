from rest_framework import serializers
from models import Pessoa,Projeto,Grupo,Aluno,Criterios,AvaliacaoGrupo,AvaliacaoAluno

class PessoaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pessoa
        fields = '__all__'


class ProjetosSerializer(serializers.ModelSerializer):

    class Meta:
        model = Projeto
        fields = '__all__'


class GrupoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Grupo
        fields = '__all__'

class AlunosSerializer(serializers.ModelSerializer):

    class Meta:
        model = Aluno
        fields ='__all__'

class CriteriosSerializer(serializers.ModelSerializer):

    class Meta:
        model = Criterios
        fields = '__all__'

class AvaliacaoGrupoSerializer(serializers.ModelSerializer):

    class Meta:
        model = AvaliacaoGrupo
        fields = ('pk','avaliador','criterio','nota','grupo')

class AvaliacaoAlunoSerializer(serializers.ModelSerializer):

    class Meta:
        model = AvaliacaoGrupo
        fields = '__all__'

