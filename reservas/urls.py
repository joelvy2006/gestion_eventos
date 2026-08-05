from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'api', views.ReservaViewSet, basename='reservas-api')

urlpatterns = [
    path('', include(router.urls)),
    path('lista/', views.lista_reservas, name='lista_reservas'),
    path('agregar/', views.agregar_reserva, name='agregar_reserva'),
    path('editar/<int:id>/', views.editar_reserva, name='editar_reserva'),
    path('confirmar/<int:id>/', views.confirmar_reserva, name='confirmar_reserva'),
    path('cancelar/<int:id>/', views.cancelar_reserva, name='cancelar_reserva'),
    path('eliminar/<int:id>/', views.eliminar_reserva, name='eliminar_reserva'),
    path('buscar/', views.buscar_espacios, name='buscar_espacios'),

    # Nueva ruta para reservar desde la página pública
    path('reservar/<int:espacio_id>/', views.reservar_espacio, name='reservar_espacio'),
]