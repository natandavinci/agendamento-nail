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