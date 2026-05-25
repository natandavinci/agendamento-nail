from django.urls import path

from .views import agendar

from .views import (
    agendar,
    horarios_disponiveis
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
]