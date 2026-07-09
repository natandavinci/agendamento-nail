import re

from django import forms

from django.core.exceptions import ValidationError

from .models import Servico


class AgendamentoForm(forms.Form):

    nome = forms.CharField(
        max_length=100
    )

    telefone = forms.CharField(
        max_length=20
    )

    email = forms.EmailField(
        required=True
    )

    servico = forms.ModelChoiceField(
        queryset=Servico.objects.all()
    )

    data = forms.DateField(
        widget=forms.DateInput(
            attrs={'type': 'date'}
        )
    )

    horario = forms.ChoiceField(
        choices=[]
    )

    horario = forms.ChoiceField(
        choices=[]
    )

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields['servico'].label_from_instance = (
            lambda obj: f'{obj.nome} — R$ {obj.preco}'
        )

    # VALIDAÇÃO NOME

    def clean_nome(self):

        nome = self.cleaned_data['nome']

        nome = nome.strip()

        if len(nome.split()) < 2:

            raise ValidationError(
                'Digite nome e sobrenome.'
            )

        if len(nome) < 5:

            raise ValidationError(
                'Nome muito curto.'
            )

        return nome

    # VALIDAÇÃO TELEFONE

    def clean_telefone(self):

        telefone = self.cleaned_data['telefone']

        telefone = re.sub(
            r'\D',
            '',
            telefone
        )

        if len(telefone) not in [10, 11]:

            raise ValidationError(
                'Telefone inválido.'
            )

        return telefone