from django import forms

from .models import Cliente, Servico


class AgendamentoForm(forms.Form):

    cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.all()
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