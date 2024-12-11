import time
from datetime import datetime, timedelta
import sys
import os

# Adiciona o diretório raiz ao sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Classes.BaseApi import Api

api = Api()

atualizar_tabela = api.dadosApi()
print(atualizar_tabela)
agora = datetime.now()
print(f"Atualizado em: {agora.strftime('%Y-%m-%d %H:%M:%S')}")

# time.sleep(20)