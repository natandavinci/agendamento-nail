from django import forms

from .models import Agendamento


class AgendamentoForm(forms.ModelForm):

    class Meta:

        model = Agendamento

        fields = [
            'cliente',
            'servico',
            'data_inicio',
        ]

        widgets = {

            'data_inicio': forms.DateTimeInput(
                attrs={'type': 'datetime-local'}
            ),

            'data_fim': forms.DateTimeInput(
                attrs={'type': 'datetime-local'}
            ),
        }