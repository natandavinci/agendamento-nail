from django.contrib import admin

from .models import (
    Servico,
    Cliente,
    Agendamento
)


@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):

    list_display = (
        'nome',
        'preco',
        'duracao',
    )


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):

    list_display = (
        'nome',
        'telefone',
        'email',
    )


@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):

    list_display = (
        'cliente',
        'servico',
        'data_inicio',
        'data_fim',
        'status',
    )

    list_filter = (
        'status',
    )

    search_fields = (
        'cliente__nome',
    )