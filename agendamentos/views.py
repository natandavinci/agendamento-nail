from django.shortcuts import render, redirect

from .forms import AgendamentoForm
from .models import Agendamento
from datetime import timedelta
from django.db.models import Q


def agendar(request):

    form = AgendamentoForm()

    erro = None

    if request.method == 'POST':

        form = AgendamentoForm(request.POST)

        if form.is_valid():

            agendamento = form.save(commit=False)

            duracao = timedelta(
                minutes=agendamento.servico.duracao
            )

            agendamento.data_fim = (
                agendamento.data_inicio + duracao
            )

            conflito = Agendamento.objects.filter(
                data_inicio=agendamento.data_inicio,
                status='CONFIRMADO'
            ).exists()

            if conflito:

                erro = 'Este horário já está ocupado.'

            else:

                agendamento.status = 'CONFIRMADO'

                agendamento.save()

                return redirect('/agendar/')

    return render(
        request,
        'agendamentos/agendar.html',
        {
            'form': form,
            'erro': erro
        }
    )