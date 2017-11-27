from django.conf.urls import url
from . import views
from django.contrib import admin
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.documentation import include_docs_urls


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', views.Login.as_view(),name='login'),


    url(r'^projetos/$',views.ProjetosView.as_view(),name='projetos'),
    url(r'^projetos/(?P<proj>[0-9]+)/$', views.ProjetosView.as_view(),name='detalhaprojeto'),
    url(r'^projetos/(?P<proj>[0-9]+)/grupos$', views.ProjetosGruposView.as_view(),name='gruposprojeto'),

    url(r'^alunos/(?P<aln>[0-9]+)/$',views.AlunosView.as_view(),name='detalhaalunos'),
    url(r'^alunos/',views.AlunosView.as_view(),name='alunos'),

    url(r'^grupos/$',views.GruposView.as_view(),name='grupos'),
    url(r'^grupos/(?P<grpo>[0-9]+)/$',views.GruposView.as_view(),name='grupos'),
    url(r'^grupos/(?P<grpo>[0-9]+)/alunos/$', views.GrupoAlunosView.as_view(),name='alunosgrupo'),


    url(r'^criterios/(?P<projeto>[0-9]+)/$',views.CriteriosView.as_view(),name='criterios'),

    url(r'^avaliacaoaluno/',views.AvaliacaoAlunoView.as_view(),name='avaliacaoaluno'),

    url(r'^avaliacaogrupo/',views.AvaliacaoGrupoView.as_view(),name='AvaliacaoGrupo'),

    url(r'^token/', obtain_jwt_token),
    url(r'^docs/', include_docs_urls(title='My API title')),

]