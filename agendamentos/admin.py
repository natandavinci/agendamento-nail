from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import (
    Servico,
    Cliente,
    Agendamento
)

admin.site.register(Servico)
admin.site.register(Cliente)
admin.site.register(Agendamento)