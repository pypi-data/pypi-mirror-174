from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('inserimento/', views.inserimento, name='inserimento'),
    path('utenti/', views.utenti, name='utenti'),
]