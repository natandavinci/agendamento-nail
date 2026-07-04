from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.db.models import Q
from .forms import AgendamentoForm
from django.http import JsonResponse
from django.utils.dateparse import parse_date
from django.contrib.auth.decorators import login_required
from .models import (
    Agendamento,
    Cliente
)
from .utils import (
    gerar_horarios,
    obter_datas_lotadas
)
#PDF
from django.http import HttpResponse

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer
)

from reportlab.lib import colors

from reportlab.lib.styles import getSampleStyleSheet

from reportlab.lib.pagesizes import A4

from reportlab.platypus.flowables import PageBreak

from django.utils.dateparse import parse_date

@login_required
def gerar_pdf_agendamentos(request):

    data_filtro = request.GET.get('data')

    if not data_filtro:

        return HttpResponse(
            'Selecione uma data.'
        )

    data = parse_date(data_filtro)

    agendamentos = Agendamento.objects.filter(

        data_inicio__date=data,
        status='CONFIRMADO'

    ).order_by('data_inicio')

    response = HttpResponse(
        content_type='application/pdf'
    )

    response['Content-Disposition'] = (
        f'attachment; '
        f'filename="agendamentos-{data}.pdf"'
    )

    doc = SimpleDocTemplate(
        response,
        pagesize=A4,
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=18,
    )

    elementos = []

    styles = getSampleStyleSheet()

    titulo = Paragraph(

        f'Lista de Agendamentos - '
        f'{data.strftime("%d/%m/%Y")}',

        styles['Title']
    )

    elementos.append(titulo)

    elementos.append(Spacer(1, 20))

    dados = [
        [
            'Horário',
            'Cliente',
            'Telefone',
            'Serviço'
        ]
    ]

    for agendamento in agendamentos:

        dados.append([

            agendamento.data_inicio.strftime('%H:%M'),

            agendamento.cliente.nome,
            
            agendamento.cliente.telefone,

            agendamento.servico.nome,
        ])

    tabela = Table(
        dados,
        colWidths=[80, 180, 140, 120]
    )

    tabela.setStyle(TableStyle([

        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2F4439')),

        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),

        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),

        ('FONTSIZE', (0, 0), (-1, -1), 10),

        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),

        ('BACKGROUND', (0, 1), (-1, -1), colors.white),

        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#E5E5E5')),

        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [
            colors.white,
            colors.HexColor('#F8F8F8')
        ]),

        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

    ]))

    elementos.append(tabela)

    doc.build(elementos)

    return response

#AGENDAR

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

@login_required
def dashboard(request):

    hoje = datetime.now().date()

    data_filtro = request.GET.get('data')

    mes_filtro = request.GET.get('mes')

    status = request.GET.get(
        'status',
        'CONFIRMADO'
    )

    agendamentos = Agendamento.objects.filter(
        status=status
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

    titulo = 'Próximos atendimentos'

    if status == 'CONCLUIDO':

        titulo = 'Atendimentos concluídos'

    elif status == 'CANCELADO':

        titulo = 'Atendimentos cancelados'
    return render(

        request,

        'agendamentos/dashboard.html',

        {

            'agendamentos': agendamentos,

            'total_hoje': total_hoje,

            'status_atual': status,

            'titulo': titulo,

        }
    )

@login_required
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

@login_required
def excluir_agendamento(

    request,
    agendamento_id

):

    agendamento = Agendamento.objects.get(

        id=agendamento_id
    )

    agendamento.delete()

    return redirect('/dashboard/')

@login_required
def concluir_agendamento(request, agendamento_id):

    agendamento = Agendamento.objects.get(
        id=agendamento_id
    )

    agendamento.status = 'CONCLUIDO'

    agendamento.save()

    return redirect('/dashboard/')

