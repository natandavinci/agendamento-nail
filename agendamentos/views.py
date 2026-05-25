from datetime import datetime, timedelta

from django.shortcuts import render, redirect
from django.db.models import Q

from .forms import AgendamentoForm
from .models import Agendamento
from .utils import gerar_horarios
from django.http import JsonResponse


def agendar(request):

    form = AgendamentoForm()

    erro = None

    horarios_disponiveis = []

    if request.method == 'POST':

        form = AgendamentoForm(request.POST)

        data = request.POST.get('data')

        if data:

            data_obj = datetime.strptime(
                data,
                '%Y-%m-%d'
            )

            horarios = gerar_horarios(data_obj)

            horarios_disponiveis = [
                (h, h) for h in horarios
            ]

            form.fields['horario'].choices = (
                horarios_disponiveis
            )

        if form.is_valid():

            cliente = form.cleaned_data['cliente']

            servico = form.cleaned_data['servico']

            data = form.cleaned_data['data']

            horario = form.cleaned_data['horario']

            data_inicio = datetime.strptime(
                f'{data} {horario}',
                '%Y-%m-%d %H:%M'
            )

            duracao = timedelta(
                minutes=servico.duracao
            )

            data_fim = data_inicio + duracao

            conflito = Agendamento.objects.filter(
                status='CONFIRMADO'
            ).filter(

                Q(data_inicio__lt=data_fim) &

                Q(data_fim__gt=data_inicio)

            ).exists()

            if conflito:

                erro = (
                    'Já existe um agendamento '
                    'nesse horário.'
                )

            else:

                Agendamento.objects.create(
                    cliente=cliente,
                    servico=servico,
                    data_inicio=data_inicio,
                    data_fim=data_fim,
                    status='CONFIRMADO'
                )

                return redirect('/agendar/')

    return render(
        request,
        'agendamentos/agendar.html',
        {
            'form': form,
            'erro': erro,
        }
    )

def horarios_disponiveis(request):

    data = request.GET.get('data')

    if not data:

        return JsonResponse([], safe=False)

    data_obj = datetime.strptime(
        data,
        '%Y-%m-%d'
    )

    horarios = gerar_horarios(data_obj)

    horarios_livres = []

    for horario in horarios:

        data_inicio = datetime.strptime(
            f'{data} {horario}',
            '%Y-%m-%d %H:%M'
        )

        data_fim = data_inicio + timedelta(hours=2)

        conflito = Agendamento.objects.filter(
            status='CONFIRMADO'
        ).filter(

            Q(data_inicio__lt=data_fim) &

            Q(data_fim__gt=data_inicio)

        ).exists()

        if not conflito:

            horarios_livres.append(horario)

    return JsonResponse(
        horarios_livres,
        safe=False
    )