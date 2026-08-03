from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('servicios/', views.servicios, name='servicios'),
    path('equipo/', views.equipo, name='equipo'),
    path('testimonios/', views.testimonios, name='testimonios'),
    path('faq/', views.faq, name='faq'),
    path('contacto/', views.contacto, name='contacto'),
]