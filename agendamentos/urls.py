from django.urls import path

from .views import agendar


urlpatterns = [

    path(
        '',
        agendar,
        name='agendar'
    ),

]