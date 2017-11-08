from django.conf.urls import url
from . import views
from django.contrib import admin


urlpatterns = [
    #url(r'^$', views.index, name='index'),
    url(r'^admin/', admin.site.urls),
    #url(r'^getpessoas/', views.getPessoas.as_view(), name='getpessoas'),
    #url(r'^cadastro/', views.CadastroPessoa.as_view(), name='cadastro'),
    url(r'^login/', views.Login.as_view(),name='login'),
    url(r'^projetos/',views.ProjetosView.as_view(),name='projetos'),
    url(r'^alunos/',views.AlunosView.as_view(),name='alunos'),
    url(r'^grupos/',views.GruposView.as_view(),name='grupos'),
    url(r'^criterios/',views.CriteriosView.as_view(),name='criterios'),
    url(r'^avaliacaoaluno/',views.AvaliacaoAlunoView.as_view(),name='avaliacaoaluno'),
    url(r'^avaliacaogrupo/',views.AvaliacaoGrupoView.as_view(),name='AvaliacaoGrupo'),
]