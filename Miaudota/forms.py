from django import forms

class ContatoForm(forms.Form):

    # Perguntas do questionário
    adotar_qualquer_animal = forms.CharField(widget=forms.Textarea, label='1 - Por que você quer adotar um animal?')
    
    todos_concordam = forms.ChoiceField(
        label='2 - Todos concordam com a adoção?',
        choices=[('sim', 'Sim'), ('nao', 'Não')],
        widget=forms.RadioSelect,
        required=True
    )
    
    animal_seria_problema = forms.ChoiceField(label='3 - Se a família resolver ter um bebê, o animal será um problema?',
    choices=[('sim', 'Sim'), ('nao', 'Não')],
    widget=forms.RadioSelect,
    required=True
    )

    possibilidade_devolucao = forms.ChoiceField(label='4 - Existe a possibilidade de devolução do animal?', 
    choices=[('sim', 'Sim'), ('nao', 'Não')],
    widget=forms.RadioSelect,
    required=True
    )
    
    despesas_preparado = forms.ChoiceField(label='5 - Você está preparado para as despesas de alimentação, higiene e veterinárias que o animal precisa ter?',
    choices=[('sim', 'Sim'), ('nao', 'Não')],
    widget=forms.RadioSelect,
    required=True
    )
    
    moradia = forms.CharField(widget=forms.Textarea, label='6 - Você mora em casa ou apartamento? Sendo casa, é murada? Sendo apê, é telado?')
    
    horas_sozinho = forms.IntegerField(
        label='7 - Quantas horas o animal ficará sozinho na residência?', 
        required=True,
        widget=forms.NumberInput(attrs={'class': 'highlight'})
    )
    
    viagens_como_ficar = forms.CharField(widget=forms.Textarea, label='8 - Em caso de viagens, com quem ficará o animal?')
    
    consciencia_castracao = forms.ChoiceField(label='9 - Você tem consciência da importância da castração?',
    choices=[('sim', 'Sim'), ('nao', 'Não')],
    widget=forms.RadioSelect,
    required=True)
    
    avisar_projeto = forms.ChoiceField(label='10 - Você concorda em avisar os membros do projeto caso aconteça algo com o animal?',
    choices=[('sim', 'Sim'), ('nao', 'Não')],
    widget=forms.RadioSelect,
    required=True
    )