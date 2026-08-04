from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'api', views.PagoViewSet, basename='pagos-api')

urlpatterns = [
    path('', include(router.urls)),
    path('lista/', views.lista_pagos, name='lista_pagos'),
    path('ver/<int:id>/', views.ver_pago, name='ver_pago'),
    path('registrar/<int:reserva_id>/', views.registrar_pago, name='registrar_pago'),
    path('editar/<int:id>/', views.editar_pago, name='editar_pago'),
    path('agregar-extra/<int:id>/', views.agregar_extra_pago, name='agregar_extra_pago'),
    path('eliminar/<int:id>/', views.eliminar_pago, name='eliminar_pago'),
]
