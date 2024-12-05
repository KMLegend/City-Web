from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Disponiveis_tabela_vendas
from .api.serializers import Disponiveis_tabela_vendasSerializer

import json

@api_view(['GET'])
def get_disponiveis(request):

    if request.method == 'GET':
        disponiveis = Disponiveis_tabela_vendas.objects.all()

        serializer = Disponiveis_tabela_vendasSerializer(disponiveis, many=True)
        return Response(serializer.data)

    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT'])
def get_empresa(request, empresa):

    try:
        emp = Disponiveis_tabela_vendas.objects.filter(empresa=empresa)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = Disponiveis_tabela_vendasSerializer(emp, many=True)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = Disponiveis_tabela_vendasSerializer(emp, data=request.data)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def disponiveis_manager(request):

    if request.method == 'GET':
        if request.method == 'GET':
            disponiveis = Disponiveis_tabela_vendas.objects.all()

            serializer = Disponiveis_tabela_vendasSerializer(disponiveis, many=True)
            return Response(serializer.data)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'POST':
        new_emp = request.data

        serializer = Disponiveis_tabela_vendasSerializer(data=new_emp)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'PUT':
        empresa = request.data['id']

        try:
            update_empresa = Disponiveis_tabela_vendas.objects.get(pk=empresa)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        print(request.data)

        serializer = Disponiveis_tabela_vendasSerializer(update_empresa, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        try:
            disponiveis = Disponiveis_tabela_vendas.objects.get(pk=request.data['id'])
            disponiveis.delete()
            return Response(status=status.HTTP_202_ACCEPTED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
