from datetime import datetime, timedelta

from .models import (
    Agendamento,
    HorarioPadrao,
    DiaBloqueado,
    HorarioBloqueado,
    HorarioExtra,
)


def gerar_horarios(data):

    # Se o dia inteiro está bloqueado, não há horários
    dia_bloqueado = DiaBloqueado.objects.filter(
        data=data
    ).exists()

    if dia_bloqueado:
        return []

    weekday = data.weekday()

    # Horários padrão ativos para esse dia da semana
    horarios_padrao = HorarioPadrao.objects.filter(
        dia_semana=weekday,
        ativo=True
    ).values_list('horario', flat=True)

    horarios = set(horarios_padrao)

    # Remove horários bloqueados pontualmente nessa data
    bloqueados = HorarioBloqueado.objects.filter(
        data=data
    ).values_list('horario', flat=True)

    horarios -= set(bloqueados)

    # Adiciona horários extras liberados pontualmente nessa data
    extras = HorarioExtra.objects.filter(
        data=data
    ).values_list('horario', flat=True)

    horarios |= set(extras)

    return sorted(horarios)


def obter_datas_lotadas():

    hoje = datetime.now().date()

    datas_lotadas = []

    for i in range(60):

        data = hoje + timedelta(days=i)

        horarios = gerar_horarios(data)

        quantidade_maxima = len(horarios)

        if quantidade_maxima == 0:

            datas_lotadas.append(
                data.strftime('%Y-%m-%d')
            )

            continue

        agendamentos = Agendamento.objects.filter(
            data_inicio__date=data,
            status='CONFIRMADO'
        ).count()

        if agendamentos >= quantidade_maxima:

            datas_lotadas.append(
                data.strftime('%Y-%m-%d')
            )

    return datas_lotadas