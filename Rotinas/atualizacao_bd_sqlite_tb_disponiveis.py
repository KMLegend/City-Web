import time
from datetime import datetime, timedelta
import sys
import os

# Adiciona o diretório raiz ao sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Classes.BaseApi import Api
import requests

api = Api()

def post(url_api):
    dados = api.tabela_disponivel()
    novos_nomes = [
        'produto',
        'empresa',
        'nome_fantasia',
        'obra',
        'unidade',
        'tipo',
        'cod_tipologia',
        'tipologia',
        'status'
    ]

    # Renomeando as colunas
    dados.columns = novos_nomes

    # Convertendo os valores nulos para um texto padrão
    dados.fillna(0, inplace=True)

    # Iterando por cada linha do DataFrame
    for _, row in dados.iterrows():
        # Criando um dicionário para cada registro
        data = {
            'produto': row['produto'],
            'empresa': row['empresa'],
            'nome_fantasia': row['nome_fantasia'],
            'obra': row['obra'],
            'unidade': row['unidade'],
            'tipo': row['tipo'],
            'cod_tipologia': row['cod_tipologia'],
            'tipologia': row['tipologia'],
            'status': row['status']
        }
        print(f"Enviando: {data}")

        # Enviando a requisição POST com o formato JSON
        response = requests.post(url_api, json=data, headers={'Content-Type': 'application/json'})

        # Exibindo a resposta para debug
        print(f"Resposta: {response.text}")

        # Retornando o código de status
    return response.status_code
def delete(url_api):
    df = api.tabela_disponivel_sqlite()
    for _, row in df.iterrows():
        response = requests.delete(url_api + str(row["id"]), headers={'Content-Type': 'application/json'})
        return response.status_code
# while True:
url_api = 'https://city-solucoes.com/api/data/'
# print(delete(url_api))
print(post(url_api))

agora = datetime.now()
print(f"Atualizado em: {agora.strftime('%Y-%m-%d %H:%M:%S')}")

    # time.sleep(4 * 60 * 60)
