import sqlite3
import time
from datetime import datetime, timedelta
import sys
import os

# Adiciona o diretório raiz ao sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Classes.BaseApi import Api
import requests

api = Api()
conexao = api.conexao_bd_sqlite()
cursor = conexao.cursor()

def post(url_api):
    dados = api.tabela_disponivel()
    novos_nomes = [
        'Produto',
        'Empresa',
        'NomeFantasia',
        'Obra',
        'Unidade',
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
            'Produto': row['Produto'],
            'Empresa': row['Empresa'],
            'NomeFantasia': row['NomeFantasia'],
            'Obra': row['Obra'],
            'Unidade': row['Unidade'],
            'tipo': row['tipo'],
            'cod_tipologia': row['cod_tipologia'],
            'tipologia': row['tipologia'],
            'status': row['status']
        }
        # print(f"Enviando: {data}")
        sql_insert = f"INSERT INTO api_disponiveis_tabela_vendas (Produto, Empresa, NomeFantasia, Obra, Unidade, tipo, cod_tipologia, tipologia, status) VALUES ('{row['Produto']}','{row['Empresa']}','{row['NomeFantasia']}','{row['Obra']}','{row['Unidade']}','{row['tipo']}','{row['cod_tipologia']}','{row['tipologia']}','{row['status']}')"
        print(sql_insert)
        cursor.execute(sql_insert)
        conexao.commit()
        # Enviando a requisição POST com o formato JSON
        # response = requests.post(url_api, json=data, headers={'Content-Type': 'application/json'})
        # print(response.status_code)
        # Exibindo a resposta para debug
        # print(f"Resposta: {response.text}")

        # Retornando o código de status
    return cursor

def delete(url_api):

    df = api.tabela_disponivel_sqlite()
    sql_drop = f"DROP TABLE api_disponiveis_tabela_vendas;"
    cursor.execute(sql_drop)
    conexao.commit()
    print(sql_drop)
    
    sql_create = f"""CREATE TABLE "api_disponiveis_tabela_vendas" (
        "id"	INTEGER,
        "Produto"	VARCHAR(255),
        "Empresa"	VARCHAR(255),
        "NomeFantasia"	VARCHAR(255),
        "Obra"	VARCHAR(255),
        "Unidade"	VARCHAR(255),
        "tipo"	VARCHAR(255),
        "cod_tipologia"	INT,
        "tipologia"	VARCHAR(255),
        "status"	VARCHAR(255),
        PRIMARY KEY("id" AUTOINCREMENT) 
    );"""
    
    cursor.execute(sql_create)
    conexao.commit()
    
    return print(sql_create)
    # print(df)
    # for _, row in df.iterrows():
    #     data = {
    #         'id': row['id']
    #     }
    #     try:
    #         sql_delete = f"TRUNCATE TABLE api_disponiveis_tabela_vendas;"
    #         print(sql_delete)
    #         cursor.execute(sql_delete)
    #         conexao.commit()
    #     except Exception as e:
    #         print(e)
            
          
    #     response = requests.delete(url_api, json=data, headers={'Content-Type': 'application/json'})


    # return response.status_code
# while True:
url_api = 'http://city-solucoes.com/api/data/'
print(delete(url_api))
print(post(url_api))

agora = datetime.now()
print(f"Atualizado em: {agora.strftime('%Y-%m-%d %H:%M:%S')}")

    # time.sleep(4 * 60 * 60)
