from django.urls import path
from . import views
urlpatterns = [
    path('publico/', views.lista_publica, name='lista_publica'),
    path('', views.lista_espacios, name='lista_espacios'),
    path('agregar/', views.agregar_espacio, name='agregar_espacio'),
    path('editar/<int:id>/', views.editar_espacio, name='editar_espacio'),
    path('eliminar/<int:id>/', views.eliminar_espacio, name='eliminar_espacio'),
]
