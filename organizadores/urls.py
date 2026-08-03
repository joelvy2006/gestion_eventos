from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_organizadores, name='lista_organizadores'),
    path('agregar/', views.agregar_organizador, name='agregar_organizador'),
    path('editar/<int:id>/', views.editar_organizador, name='editar_organizador'),
    path('eliminar/<int:id>/', views.eliminar_organizador, name='eliminar_organizador'),
]