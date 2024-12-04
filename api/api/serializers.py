from rest_framework import serializers

from api.models import Disponiveis_tabela_vendas

class Disponiveis_tabela_vendasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disponiveis_tabela_vendas
        fields = '__all__'