from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'api', views.OrganizadorViewSet, basename='organizadores-api')

urlpatterns = [
    path('', include(router.urls)),
    path('lista/', views.lista_organizadores, name='lista_organizadores'),
    path('agregar/', views.agregar_organizador, name='agregar_organizador'),
    path('editar/<int:id>/', views.editar_organizador, name='editar_organizador'),
    path('eliminar/<int:id>/', views.eliminar_organizador, name='eliminar_organizador'),
]