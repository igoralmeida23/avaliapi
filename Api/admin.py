
from __future__ import unicode_literals
from models import Pessoa
from models import Professor
from models import Avaliador
from models import Aluno
from models import Projeto
from models import Disciplinas
from models import Etapas
from models import Grupo
from models import Entregas
from models import Apresentacao
from models import Criterios
from models import Avaliacao
from models import AvaliacaoAluno
from models import AvaliacaoGrupo
from django.contrib import admin


admin.site.register(Pessoa)
admin.site.register(Professor)
admin.site.register(Avaliador)
admin.site.register(Aluno)
admin.site.register(Projeto)
admin.site.register(Disciplinas)
admin.site.register(Etapas)
admin.site.register(Grupo)
admin.site.register(Entregas)
admin.site.register(Apresentacao)
admin.site.register(Criterios)
admin.site.register(Avaliacao)
admin.site.register(AvaliacaoAluno)
admin.site.register(AvaliacaoGrupo)
