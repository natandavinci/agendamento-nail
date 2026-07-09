from django.contrib import admin

from .models import (
    Servico,
    Cliente,
    Agendamento,
    HorarioPadrao,
    DiaBloqueado,
    HorarioBloqueado,
    HorarioExtra,
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

@admin.register(HorarioPadrao)
class HorarioPadraoAdmin(admin.ModelAdmin):

    list_display = (
        'dia_semana',
        'horario',
        'ativo',
    )

    list_filter = (
        'dia_semana',
        'ativo',
    )

    ordering = (
        'dia_semana',
        'horario',
    )


@admin.register(DiaBloqueado)
class DiaBloqueadoAdmin(admin.ModelAdmin):

    list_display = (
        'data',
        'motivo',
    )

    ordering = (
        'data',
    )


@admin.register(HorarioBloqueado)
class HorarioBloqueadoAdmin(admin.ModelAdmin):

    list_display = (
        'data',
        'horario',
    )

    ordering = (
        'data',
        'horario',
    )


@admin.register(HorarioExtra)
class HorarioExtraAdmin(admin.ModelAdmin):

    list_display = (
        'data',
        'horario',
    )

    ordering = (
        'data',
        'horario',
    )