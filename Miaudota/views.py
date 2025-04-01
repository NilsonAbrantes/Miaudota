from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, logout as auth_logout

def registro_ong(request):
  if request.method == 'POST':
    username = request.POST['username']
    senha = request.POST['senha']
    email = request.POST['email']

    user = User.objects.create_user(username=username, email=email, password=senha)
    grupo_ong = Group.objects.get(name='ong')
    user.groups.add(grupo_ong)

    login(request, user)
    return redirect('html/dashboard_ong')

  return render(request, 'html/registro_ong.html')

def registro_adotante(request):
  if request.method == 'POST':
    username = request.POST['username']
    senha = request.POST['senha']
    email = request.POST['email']

    user = User.objects.create_user(username=username, email=email, password=senha)
    grupo_adotante = Group.objects.get(name='adotante')
    user.groups.add(grupo_adotante)

    login(request, user)
    return redirect('home')

  return render(request, 'html/registro_adotante.html') 

def login_view(request):
  if request.method == 'POST':
    username = request.POST['username']
    senha = request.POST['senha']

    user = authenticate(request, username=username, password=senha)
    if user is not None:
      auth_login(request, user)

      #verifica o grupo
      if user.is_superuser:
        return redirect('/admin/')
      elif user.groups.filter(name='ong').exists():
        return redirect('/dashboard_ong')
      elif user.groups.filter(name='adotante').exists():
        return redirect('/home')
      else:
        return redirect('/home')
      
    else:
      messages.error(request, 'Usuário ou senha Inválidos.')
  
  return render(request, 'html/login.html')

def logout_view(request):
  auth_logout(request)
  return redirect('/login')

@login_required
def dashboard_ong(request):
    return render(request, 'html/dashboard_ong.html')

@login_required
def home(request):
    return render(request, 'html/home.html')
