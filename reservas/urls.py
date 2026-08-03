from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_reservas, name='lista_reservas'),
    path('agregar/', views.agregar_reserva, name='agregar_reserva'),
    path('editar/<int:id>/', views.editar_reserva, name='editar_reserva'),
    path('confirmar/<int:id>/', views.confirmar_reserva, name='confirmar_reserva'),
    path('cancelar/<int:id>/', views.cancelar_reserva, name='cancelar_reserva'),
    path('eliminar/<int:id>/', views.eliminar_reserva, name='eliminar_reserva'),
]
