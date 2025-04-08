from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, logout as auth_logout
from .models import Animal, Ong
from django.core.exceptions import PermissionDenied

def registro_ong(request):
    if request.method == 'POST':
        username = request.POST['username']
        senha = request.POST['senha']
        email = request.POST['email']

        user = User.objects.create_user(username=username, email=email, password=senha)
        grupo_ong = Group.objects.get(name='ong')
        user.groups.add(grupo_ong)

        auth_login(request, user)
        return redirect('dashboard_ong')

    return render(request, 'html/login/registro_ong.html')

def registro_adotante(request):
    if request.method == 'POST':
        username = request.POST['username']
        senha = request.POST['senha']
        email = request.POST['email']

        user = User.objects.create_user(username=username, email=email, password=senha)
        grupo_adotante = Group.objects.get(name='adotante')
        user.groups.add(grupo_adotante)

        auth_login(request, user)
        return redirect('dashboard_adotante')

    return render(request, 'html/login/registro_adotante.html') 

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        senha = request.POST['senha']

        user = authenticate(request, username=username, password=senha)
        if user is not None:
            auth_login(request, user)

            if user.is_superuser:
                return redirect('/admin/')
            elif user.groups.filter(name='ong').exists():
                return redirect('dashboard_ong')
            elif user.groups.filter(name='adotante').exists():
                return redirect('dashboard_adotante')
            else:
                return redirect('login')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')

    return render(request, 'html/login/login.html')

def logout_view(request):
    auth_logout(request)
    return redirect('login')

@login_required
def dashboard_ong(request):
    return render(request, 'html/dashboard/dashboard_ong.html')

@login_required
def dashboard_adotante(request):
    return render(request, 'html/dashboard/dashboard_adotante.html')

@login_required
def home(request):
    return render(request, 'html/dashboard/home.html')

#somente ongs podem realizar algumas operações
def checar_ong(user):
    return user.groups.filter(name='ong').exists()

@login_required
def lista_animais(request):
    if not checar_ong(request.user):
        raise PermissionDenied

    ong = Ong.objects.get(user=request.user)
    animais = Animal.objects.filter(ong=ong)
    return render(request, 'html/animais/lista.html',{'animais':animais})

@login_required
def adicionar_animais(request):
    if not checar_ong(request.user):
        raise PermissionDenied
    
    if request.method == 'POST':
        nome = request.POST['nome']
        especie = request.POST['especie']
        raca = request.POST['raca']
        idade = request.POST['idade']
        sexo = request.POST['sexo']
        descricao = request.POST['descricao']
        foto = request.FILES['foto']

        ong = Ong.objects.get(user=request.user)
        Animal.objects.create(
            nome=nome,
            especie=especie,
            raca=raca,
            idade=idade,
            sexo=sexo,
            descricao=descricao,
            foto=foto,
            ong=ong,
            disponivel=True
        )
        return redirect('lista_animais')
    
    return render(request, 'html/animais/adicionar.html')

@login_required
def editar_animal(request, animal_id):
    if not checar_ong(request.user):
        raise PermissionDenied
    
    animal = Animal.objects.get(id=animal_id)

    if request.method == 'POST':
        animal.nome = request.POST['nome']
        animal.especie = request.POST['especie']
        animal.raca = request.POST['raca']
        animal.idade = request.POST['idade']
        animal.sexo = request.POST['sexo']
        animal.descricao = request.POST['descricao']
        animal.disponivel = request.POST('disponivel','off') == 'on'
        if 'foto' in request.FILES:
            animal.foto = request.FILES['foto']
        animal.save()
        return redirect('lista_animais')
    
    return render(request, 'html/animais/editar.html', {'animal':animal})

@login_required
def excluir_animal(request, animal_id):
    if not checar_ong(request.user):
        raise PermissionDenied
    
    animal = Animal.objects.get(id=animal_id)
    animal.delete()
    return redirect('lista_animais')

def listar_animais_publicos(request):
    animais = Animal.objects.filter(disponivel=True)
    return render(request, 'html/animais/publicos.html', {'animais':animais})