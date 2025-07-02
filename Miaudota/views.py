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
        email = request.POST['email']
        senha = request.POST['senha']
        cpf = request.POST['cpf']
        data_nascimento = request.POST['data_nascimento']  
        telefone = request.POST['telefone']
        endereco = request.POST['endereco']

        # Criando o usuário
        user = User.objects.create_user(username=username, email=email, password=senha)
        user.save()
        
        #Adicionando ao grupo de Adotante
        grupo_adotante = Group.objects.get(name='adotante')
        user.groups.add(grupo_adotante)

        # Criando o objeto Adotante associado ao usuário
        adotante = Adotante.objects.create(
        user=user,
        nome=username,
        cpf=cpf,
        data_nascimento=data_nascimento,
        telefone=telefone,
        endereco=endereco)
        adotante.save()


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
    ong = Ong.objects.get(user=request.user)
    return render(request, 'html/dashboard/dashboard_ong.html', {'ong':ong})

@login_required
def dashboard_adotante(request):
    try:
        # Obtendo o adotante associado ao usuário logado
        adotante = Adotante.objects.get(user=request.user)
        
        # Recuperando os animais disponíveis (que podem ser adotados)
        animais = Animal.objects.filter(disponivel=True)  
        
        # Passando o adotante e os animais para o template
        return render(request, 'html/dashboard/dashboard_adotante.html', {'adotante': adotante, 'animais': animais})
    
    except Adotante.DoesNotExist:
        # Caso o adotante não exista, cria um novo adotante
        adotante = Adotante.objects.create(user=request.user, nome=request.user.username)
        animais = []  # Ou um valor padrão

        return render(request, 'html/dashboard/dashboard_adotante.html', {'adotante': adotante, 'animais': animais})


def home(request):
    animais = Animal.objects.filter(disponivel=True)
    for animal in animais:
        animal.tags = animal.descricao.split(",")
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

def mascara_cpf(cpf):
    return f"{cpf[:3]}.***.***-{cpf[-2:]}"

@login_required
def contato_ong(request, animal_id, adotante_id):
    try:
        animal = Animal.objects.get(id=animal_id)
        adotante = Adotante.objects.get(id=adotante_id)
        cpf_mascarado = mascara_cpf(adotante.cpf)
        
        if request.method == 'POST':
            form = ContatoForm(request.POST)
            if form.is_valid():
               # Acesso os dados do formulário
                adotar_qualquer_animal = form.cleaned_data['adotar_qualquer_animal']
                todos_concordam = form.cleaned_data['todos_concordam']
                animal_seria_problema = form.cleaned_data['animal_seria_problema']
                possibilidade_devolucao = form.cleaned_data['possibilidade_devolucao']
                despesas_preparado = form.cleaned_data['despesas_preparado']
                moradia = form.cleaned_data['moradia']
                horas_sozinho = form.cleaned_data['horas_sozinho']
                viagens_como_ficar = form.cleaned_data['viagens_como_ficar']
                consciencia_castracao = form.cleaned_data['consciencia_castracao']
                avisar_projeto = form.cleaned_data['avisar_projeto']

                # Corpo do e-mail com as respostas
                corpo_mensagem = f"""
                1 - Por que você quer adotar um animal? {adotar_qualquer_animal}
                2 - Todos concordam com a adoção? {'Sim' if todos_concordam else 'Não'}
                3 - Se a família resolver ter um bebê, o animal será um problema? {'Sim' if animal_seria_problema else 'Não'}
                4 - Existe a possibilidade de devolução do animal? {'Sim' if possibilidade_devolucao else 'Não'}
                5 - Você está preparado para as despesas de alimentação, higiene e veterinárias que o animal precisa ter? {'Sim' if despesas_preparado else 'Não'}
                6 - Você mora em casa ou apartamento? Sendo casa, é murada? Sendo apê, é telado? {moradia}
                7 - Quantas horas o animal ficará sozinho na residência? {horas_sozinho}
                8 - Em caso de viagens, com quem ficará o animal? {viagens_como_ficar}
                9 - Você tem consciência da importância da castração? {'Sim' if consciencia_castracao else 'Não'}
                10 - Você concorda em avisar os membros do projeto caso aconteça algo com o animal? {'Sim' if avisar_projeto else 'Não'}
                """

                # Enviar o e-mail
                send_mail(
                    f'Contato sobre o animal: {animal.nome}',
                    corpo_mensagem,
                    adotante.email,
                    [animal.ong.user.email],
                    fail_silently=False,
                )

                messages.success(request, 'Sua mensagem foi enviada com sucesso! A ONG entrará em contato em breve.')
                return redirect('animais_publicos')
        else:
            form = ContatoForm()

        return render(request, 'html/animais/contato.html', {'form': form, 'animal': animal, 'adotante': adotante, 'cpf_mascarado': cpf_mascarado})

    except Animal.DoesNotExist:
        raise PermissionDenied("Animal não encontrado.")
    except Adotante.DoesNotExist:
        raise PermissionDenied("Adotante não encontrado.")

