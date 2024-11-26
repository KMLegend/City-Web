from django.shortcuts import render
from django.http import Http404, JsonResponse, HttpResponse
from Classes.BaseApi import Api
from django.contrib.auth.models import User


def index(request):
    return render(request, "hubPrincipal/index.html")
