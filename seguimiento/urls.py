from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_pagos, name='lista_pagos'),
    path('ver/<int:id>/', views.ver_pago, name='ver_pago'),
    path('registrar/<int:reserva_id>/', views.registrar_pago, name='registrar_pago'),
]
