from django.shortcuts import render
from django.http import Http404, JsonResponse, HttpResponse
from Classes.BaseApi import Api
from django.contrib.auth.models import User

from .models import Perguntas


def index(request):
    latest_question_list = Perguntas.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "portalCorretoresHypno/index.html", context)

def dados_api(request):
    api = Api()
    json = api.dadosApi()
    return JsonResponse(json, safe=False)
