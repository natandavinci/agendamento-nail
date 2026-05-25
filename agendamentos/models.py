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

    STATUS = (
        ('PENDENTE', 'Pendente'),
        ('CONFIRMADO', 'Confirmado'),
        ('CANCELADO', 'Cancelado'),
    )

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
        choices=STATUS,
        default='PENDENTE'
    )

    google_event_id = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f'{self.cliente} - {self.data_inicio}'