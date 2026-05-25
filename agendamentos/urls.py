from django.urls import path
from .views import (
    agendar,
    horarios_disponiveis,
    datas_bloqueadas
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
]