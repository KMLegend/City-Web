import time
from datetime import datetime, timedelta
import sys
import os

# Adiciona o diretório raiz ao sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Classes.BaseApi import Api
import requests

api = Api()

while True:
    url = 'https://city-solucoes.com'
    atualizar_tabela = api.tabela_disponivel_sqlite()

    agora = datetime.now()
    print(f"Atualizado em: {agora.strftime('%Y-%m-%d %H:%M:%S')}")

    time.sleep(4 * 60 * 60)