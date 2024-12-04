from django.urls import include, path

from . import views
urlpatterns = [
    path('empreendimentos', views.get_disponiveis, name='get_disponiveis'),
    path('empreendimentos/<str:empresa>', views.get_empresa, name='get_empresa'),
    path('data/', views.disponiveis_manager, name='get_data'),
]
