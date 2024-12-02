from django.shortcuts import render
from django.template import loader
from django.http import Http404, JsonResponse, HttpResponse
from Classes.BaseApi import Api
from django.contrib.auth.models import User

from .models import Perguntas


def index(request):
    return render(request, "portalCorretoresHypno/index.html")

def dados_api(request):
    api = Api()
    json = api.dadosApi()
    return JsonResponse(json, safe=False)
