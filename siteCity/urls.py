
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path("tabela-de-vendas/", include("portalCorretoresHypno.urls")),
    path('', include("home.urls")),

    path('api/', include("api.urls"), name='apí_rest_url')
]
