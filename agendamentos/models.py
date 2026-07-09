from django.db import models

# Create your models here.
from django.db import models


class Servico(models.Model):

    nome = models.CharField(max_length=100)

    preco = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    duracao = models.IntegerField(
        default=120,
        help_text='Duração em minutos'
    )

    def __str__(self):
        return self.nome
    

#CLIENTE    
class Cliente(models.Model):

    nome = models.CharField(max_length=100)

    telefone = models.CharField(max_length=20)

    email = models.EmailField(
        blank=True,
        null=True
    )

    def __str__(self):
        return self.nome
    
#AGENDAMENTO
class Agendamento(models.Model):

    STATUS_CHOICES = [

        ('CONFIRMADO', 'Confirmado'),

        ('CONCLUIDO', 'Concluído'),

        ('CANCELADO', 'Cancelado'),

    ]

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE
    )

    servico = models.ForeignKey(
        Servico,
        on_delete=models.CASCADE
    )

    data_inicio = models.DateTimeField()

    data_fim = models.DateTimeField()

    status = models.CharField(

        max_length=20,

        choices=STATUS_CHOICES,

        default='CONFIRMADO'
    )

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return (
            f'{self.cliente.nome} - '
            f'{self.data_inicio}'
        )
    

# HORÁRIO PADRÃO (agenda-base, recorrente por dia da semana)
class HorarioPadrao(models.Model):

    DIAS_SEMANA = [
        (0, 'Segunda'),
        (1, 'Terça'),
        (2, 'Quarta'),
        (3, 'Quinta'),
        (4, 'Sexta'),
        (5, 'Sábado'),
        (6, 'Domingo'),
    ]

    dia_semana = models.IntegerField(choices=DIAS_SEMANA)

    horario = models.CharField(max_length=5)

    ativo = models.BooleanField(default=True)

    class Meta:
        unique_together = ('dia_semana', 'horario')
        ordering = ['dia_semana', 'horario']

    def __str__(self):
        return f'{self.get_dia_semana_display()} - {self.horario}'


# DIA BLOQUEADO (fecha um dia específico, mesmo sendo dia útil normalmente)
class DiaBloqueado(models.Model):

    data = models.DateField(unique=True)

    motivo = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    def __str__(self):
        return f'{self.data} - {self.motivo or "Bloqueado"}'


# HORÁRIO BLOQUEADO (fecha um horário específico dentro de um dia específico)
class HorarioBloqueado(models.Model):

    data = models.DateField()

    horario = models.CharField(max_length=5)

    class Meta:
        unique_together = ('data', 'horario')

    def __str__(self):
        return f'{self.data} {self.horario}'


# HORÁRIO EXTRA (abre um horário fora do padrão, só naquele dia específico)
class HorarioExtra(models.Model):

    data = models.DateField()

    horario = models.CharField(max_length=5)

    class Meta:
        unique_together = ('data', 'horario')

    def __str__(self):
        return f'{self.data} {self.horario}'