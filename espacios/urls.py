from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.EspacioViewSet, basename='espacios-api')

urlpatterns = [
    path('api/', include(router.urls)),

    path('', views.lista_espacios, name='lista_espacios'),
    path('publico/', views.lista_publica, name='lista_publica'),
    path('lista/', views.lista_espacios, name='lista_espacios'),
    path('agregar/', views.agregar_espacio, name='agregar_espacio'),
    path('editar/<int:id>/', views.editar_espacio, name='editar_espacio'),
    path('eliminar/<int:id>/', views.eliminar_espacio, name='eliminar_espacio'),
]
