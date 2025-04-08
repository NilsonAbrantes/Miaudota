from django import forms

class ContatoForm(forms.Form):
    nome = forms.CharField(max_length=100, label='Seu Nome')
    email = forms.EmailField(label='Seu E-mail')
    mensagem = forms.CharField(widget=forms.Textarea, label='Sua Mensagem')

class OngValida(forms.Form):
    nome = forms.CharField(max_length=100, label='Nome da Ong')
    email = forms.EmailField(label='Seu E-mail')
    cnpj = forms.CharField(max_length=18, label='Cnpj')
    telefone = forms.CharField(max_length=15, label='Telefone')
    endereco = forms.CharField(widget=forms.Textarea, label='Endereço')