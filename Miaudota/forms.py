from django import forms

class ContatoForm(forms.Form):
    nome = forms.CharField(max_length=100, label='Seu Nome')
    email = forms.EmailField(label='Seu E-mail')
    mensagem = forms.CharField(widget=forms.Textarea, label='Sua Mensagem')
