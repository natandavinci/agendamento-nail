from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.db.models import Q
from .forms import AgendamentoForm
from django.http import JsonResponse
from django.utils.dateparse import parse_date
from .models import (
    Agendamento,
    Cliente
)
from .utils import (
    gerar_horarios,
    obter_datas_lotadas
)

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

            nome = form.cleaned_data['nome']

            telefone = form.cleaned_data['telefone']

            email = form.cleaned_data['email']

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

                cliente, criado = Cliente.objects.get_or_create(

                    telefone=telefone,

                    defaults={

                        'nome': nome,

                        'email': email

                    }
                )

                Agendamento.objects.create(
                    cliente=cliente,
                    servico=servico,
                    data_inicio=data_inicio,
                    data_fim=data_fim,
                    status='CONFIRMADO'
                )

                return render(

                    request,

                    'agendamentos/confirmacao.html',

                    {

                        'cliente': cliente,

                        'servico': servico,

                        'data_inicio': data_inicio,
                        
                        'endereco': (
                            'Rua Antonio Alves Costa, 525 - Zezinho Costa - Várzea Alegre (CE)'
                        )

                    }
                )

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

def datas_bloqueadas(request):

    datas = obter_datas_lotadas()

    return JsonResponse(
        datas,
        safe=False
    )

def dashboard(request):

    hoje = datetime.now().date()

    data_filtro = request.GET.get('data')

    mes_filtro = request.GET.get('mes')

    agendamentos = Agendamento.objects.filter(
        status='CONFIRMADO'
    )

    if data_filtro:

        data = parse_date(data_filtro)

        agendamentos = agendamentos.filter(

            data_inicio__date=data
        )

    elif mes_filtro:

        ano, mes = mes_filtro.split('-')

        agendamentos = agendamentos.filter(

            data_inicio__year=ano,
            data_inicio__month=mes
        )

    else:

        agendamentos = agendamentos.filter(

            data_inicio__date__gte=hoje
        )

    agendamentos = agendamentos.order_by(
        'data_inicio'
    )

    total_hoje = Agendamento.objects.filter(

        data_inicio__date=hoje,
        status='CONFIRMADO'

    ).count()

    return render(

        request,

        'agendamentos/dashboard.html',

        {

            'agendamentos': agendamentos,

            'total_hoje': total_hoje,

        }
    )

def cancelar_agendamento(

    request,
    agendamento_id

):

    agendamento = Agendamento.objects.get(

        id=agendamento_id
    )

    agendamento.status = 'CANCELADO'

    agendamento.save()

    return redirect('/dashboard/')

def excluir_agendamento(

    request,
    agendamento_id

):

    agendamento = Agendamento.objects.get(

        id=agendamento_id
    )

    agendamento.delete()

    return redirect('/dashboard/')

def concluir_agendamento(request, agendamento_id):

    agendamento = Agendamento.objects.get(
        id=agendamento_id
    )

    agendamento.status = 'CONCLUIDO'

    agendamento.save()

    return redirect('/dashboard/')