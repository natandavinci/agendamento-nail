from django.urls import path
from .views import (
    agendar,
    horarios_disponiveis,
    datas_bloqueadas,
    dashboard,
    cancelar_agendamento,
    excluir_agendamento
)

urlpatterns = [

    path(
        '',
        agendar,
        name='agendar'
    ),

    path(
        'horarios/',
        horarios_disponiveis,
        name='horarios_disponiveis'
    ),

    path(
    'datas-bloqueadas/',
    datas_bloqueadas,
    name='datas_bloqueadas'
    ),

    path(
        'dashboard/',
        dashboard,
        name='dashboard'
    ),

    path(

        'cancelar/<int:agendamento_id>/',

        cancelar_agendamento,

        name='cancelar_agendamento'

    ),

    path(

        'excluir/<int:agendamento_id>/',

        excluir_agendamento,

        name='excluir_agendamento'

    ),

    
    ]