import sys
import os

# Adiciona o diretório raiz ao sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Classes.BaseApi import Api

api = Api()

teste = api.dadosApi()
print(teste)