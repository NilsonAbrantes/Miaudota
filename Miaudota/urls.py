from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registrar/ong/', views.registro_ong, name='registro_ong'),
    path('registrar/adotante/', views.registro_adotante, name='registro_adotante'),
    path('dashboard/ong/', views.dashboard_ong, name='dashboard_ong'),
    path('dashboard/adotante/', views.dashboard_adotante, name='dashboard_adotante'),
    path('animais/', views.lista_animais, name='lista_animais'),
    path('animais/adicionar/', views.adicionar_animais, name='adicionar_animais'),
    path('animais/<int:animal_id>/editar/', views.editar_animal, name='editar_animal'),
    path('animais/<int:animal_id>/excluir/',views.excluir_animal, name='excluir_animal'),
    path('animais/publicos', views.listar_animais_publicos, name='animais_publicos'),
    path('animais/<int:animal_id>/contato/<int:adotante_id>/', views.contato_ong, name='contato_ong'),

]

