from django.urls import path
from . import views

urlpatterns = [
    path('registrar/ong/', views.registro_ong, name='registro_ong'),
    path('registrar/adotante/', views.registro_adotante, name='registro_adotante'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/ong/', views.dashboard_ong, name='dashboard_ong'),
    path('', views.home, name='home'),
]
