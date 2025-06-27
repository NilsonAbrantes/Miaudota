from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, logout as auth_logout
from .models import Animal, Ong, Adotante
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from .forms import ContatoForm

def registro_ong(request):
    if request.method == 'POST':
        # Obtendo os dados do formulário
        print(request.POST)
        username = request.POST['username']
        senha = request.POST['senha']
        email = request.POST['email']
        cnpj = request.POST['cnpj']
        endereco = request.POST['endereco']
        telefone = request.POST['telefone']


        try:
            # Enviar e-mail ao administrador para notificar sobre o novo cadastro
            adm_email = 'lucasnilson624@gmail.com'  # E-mail do admin

            # Corpo do e-mail
            message = f'''
            Uma nova ONG está tentando se registrar no sistema. Confira os dados abaixo para validação:

            Nome de usuário: {username}
            E-mail: {email}
            Cnpj: {cnpj}
            Endereço: {endereco}
            Telefone: {telefone}
            '''

            # Enviar e-mail ao admin
            send_mail(
                'Cadastro de Nova ONG: Validação Necessária',  # Assunto
                message,  # Corpo do e-mail
                'noreply@seusite.com',  # E-mail de origem (use um e-mail válido configurado no Django)
                [adm_email],  # E-mail do admin
                fail_silently=False,
            )

            # Criar o usuário para a ONG, mas **não a salva ainda**
            user = User.objects.create_user(username=username, email=email, password=senha)
            user.is_active = False  # Define o usuário como inativo até a aprovação
            user.save()

            # Adiciona o usuário ao grupo "ong" após a criação
            grupo_ong = Group.objects.get(name='ong')
            user.groups.add(grupo_ong)

            # Criar a instância da ONG associada ao usuário
            ong = Ong.objects.create(user=user)
            ong.save()

            # Redirecionar o usuário para uma página informando que a ONG está aguardando aprovação
            messages.success(request, 'Sua ONG foi registrada com sucesso. Aguardando aprovação do administrador.')
            return redirect('/')

        except Exception as e:
            print(f"Erro ao registrar ONG: {e}")
            raise PermissionDenied("Ocorreu um erro ao tentar registrar a ONG.")

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
        messages.success(request, 'Agora Você Pode Adotar')
        return redirect('/')

    return render(request, 'html/login/registro_adotante.html') 

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)

            if user.is_superuser:
                return redirect('/admin/')
            elif user.groups.filter(name='ong').exists():
                return redirect('/dashboard/ong/')
            elif user.groups.filter(name='adotante').exists():
                return redirect('/dashboard/adotante/')
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
    animais = Animal.objects.filter(disponivel=True)
    return render(request, 'html/dashboard/dashboard_adotante.html', {'animais':animais})

def home(request):
    animais = Animal.objects.filter(disponivel=True)
    return render(request, 'html/dashboard/home.html', {'animais':animais})

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
        return redirect('dashboard_ong')
    
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

@login_required
def contato_ong(request, animal_id, adotante_id):
    try:
        # Obtendo o animal pelo ID
        animal = Animal.objects.get(id=animal_id)
        adotante = Adotante.objects.get(id=adotante_id)
        # Verifique se o animal tem uma ONG associada
        if not animal.ong:
            raise PermissionDenied("Este animal não está associado a uma ONG válida.")
        
        # Se a ONG estiver corretamente associada, você pode acessar seu e-mail
        ong_email = animal.ong.user.email  # Acessando o e-mail da ONG

        # Se o método for POST, o formulário foi enviado
        if request.method == 'POST':
            form = ContatoForm(request.POST)
            if form.is_valid():
                nome = ...
                email = form.cleaned_data['email']
                mensagem = form.cleaned_data['mensagem']

                # Envia o e-mail para a ONG
                send_mail(
                    f'Contato sobre o animal: {animal.nome}',
                    f'Nome: {nome}\nEmail: {email}\n\nMensagem:\n{mensagem}',
                    email,  # E-mail do remetente
                    [ong_email],  # E-mail da ONG
                    fail_silently=False,
                )

                messages.success(request, 'Sua mensagem foi enviada com sucesso! A ONG entrará em contato em breve.')

                # Redireciona para a página de visualização pública após envio
                return redirect('animais_publicos')

        else:
            # Se o método for GET, o formulário é renderizado vazio
            form = ContatoForm()

        # Renderiza a página do formulário de contato
        return render(request, 'html/animais/contato.html', {'form': form, 'animal': animal})

    except Animal.DoesNotExist:
        raise PermissionDenied("Animal não encontrado.")
    except Exception as e:
        print(f"Erro inesperado: {e}")

