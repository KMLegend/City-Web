from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("dados", views.dados_api, name="dados")
]

