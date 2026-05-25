from datetime import datetime


def gerar_horarios(data):

    weekday = data.weekday()

    horarios = []

    # Segunda a sexta
    if weekday in [0, 1, 2, 3, 4]:

        horarios = [
            '14:00',
            '16:00',
        ]

    # Sábado
    elif weekday == 5:

        horarios = [
            '08:00',
            '10:00',
            '14:00',
            '16:00',
        ]

    return horarios

from datetime import timedelta

from .models import Agendamento


def obter_datas_lotadas():

    hoje = datetime.now().date()

    datas_lotadas = []

    for i in range(60):

        data = hoje + timedelta(days=i)

        weekday = data.weekday()

        # Domingo
        if weekday == 6:

            datas_lotadas.append(
                data.strftime('%Y-%m-%d')
            )

            continue

        horarios = gerar_horarios(data)

        quantidade_maxima = len(horarios)

        agendamentos = Agendamento.objects.filter(
            data_inicio__date=data,
            status='CONFIRMADO'
        ).count()

        if agendamentos >= quantidade_maxima:

            datas_lotadas.append(
                data.strftime('%Y-%m-%d')
            )

    return datas_lotadas