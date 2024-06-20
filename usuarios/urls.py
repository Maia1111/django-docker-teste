from django.urls import path
from . import views


urlpatterns = [
    path('login', views.login_view, name='login_view'),
    path('sair', views.logout_view, name='sair'),
    path('criar_usuario/', views.criar_usuario, name='criar_usuario'),
    path('completar_dados/', views.completar_dados, name='completar_dados'),
    path('upload_foto/', views.upload_foto, name='upload_foto'),
    path('mudar_senha/', views.mudar_senha, name='mudar_senha'),
    path('home/', views.home, name='home'),
    path('admin_usuarios/', views.admin_usuarios, name='admin_usuarios'),
    path('aguarde_validacao/', views.aguarde_validacao, name='aguarde_validacao'),
    path('recuperacao_senha/', views.recuperacao_senha, name='recuperacao_senha'),
    path('mensagem_recuperacao_senha/', views.mensagem_recuperacao_senha, name='mensagem_recuperacao_senha'),
    path('listar_usuarios_validar/', views.listar_usuarios_validar, name='listar_usuarios_validar'),
    path('validar_usuario/<int:id>/', views.validar_usuario, name='validar_usuario'),
    path('ver_detalhe_usuario_validar/<int:id>/', views.ver_detalhe_usuario_validar, name='ver_detalhe_usuario_validar'),
    path('usuarios_validados/', views.usuarios_validados, name='usuarios_validados'),
    path('rejeitar_validacao/<int:id>/', views.rejeitar_validacao, name='rejeitar_validacao'),

   
    
]
