from django.db import models
from django.contrib.auth.models import User

class Ong(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE) #on_delete=models.CASCADE significa que se o usuário for deletado, a ONG associada também será deletada.
    nome = models.CharField(max_length=100)
    cpnj = models.CharField(max_length=18)
    telefone = models.CharField(max_length=15)
    endereco = models.TextField()
    
    #Esse método define o que será exibido quando o objeto da ONG for mostrado como string (ex: no admin do Django ou no terminal).  
    #👉 Isso faz com que apareça o **nome da ONG** ao invés de algo genérico como `Ong object (1)`.
    def __str__(self):
        return self.nome

class Animal(models.Model):
    SEXO_CHOICES = (
        ('M', 'Macho'),
        ('F', 'Fêmea'),
    )
    nome = models.CharField(max_length=100)
    especie = models.CharField(max_length=50)
    raca = models.CharField(max_length=50)
    idade = models.PositiveSmallIntegerField()
    sexo = models.CharField(max_length=1 , choices=SEXO_CHOICES)
    descricao = models.TextField()
    foto = models.ImageField(upload_to='animais/')
    disponivel = models.BooleanField(default=True)
    #Cria um campo de chave estrangeira (ForeignKey), que representa uma ligação entre esse modelo e o modelo Ong.
    # 👉 Isso significa que muitos registros desse modelo podem estar associados a uma única ONG.
    ong = models.ForeignKey(Ong, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome
    
class Adotante(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Relacionamento com o usuário
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11, unique=True)  
    telefone = models.CharField(max_length=15)
    endereco = models.TextField()
    data_nascimento = models.DateField()
    consentimento = models.BooleanField()

    def __str__(self):
        return self.nome