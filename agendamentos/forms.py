from django import forms

from .models import Servico


class AgendamentoForm(forms.Form):

    nome = forms.CharField(
        max_length=100
    )

    telefone = forms.CharField(
        max_length=20
    )

    email = forms.EmailField(
        required=False
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