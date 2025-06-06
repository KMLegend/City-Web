import pandas as pd
import json
import pyodbc
import datetime
from shareplum import Site, Office365
from shareplum.site import Version
import sqlite3

def converter_para_serializavel(obj):
        if isinstance(obj, pd.Timestamp):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()
        raise TypeError(f"Tipo não serializável: {type(obj)}")

authcookie = Office365('https://cityinc123.sharepoint.com', username='inovacao.sistemas@cityinc.com.br',
                               password='Zat41304').GetCookies()
site = Site('https://cityinc123.sharepoint.com/inovacao-sistemas/', version=Version.v365, authcookie=authcookie)

pasta = site.Folder('Documentos Compartilhados/Compartilhado/Comercial')
df_tabela_vendas = pd.read_excel(pasta.get_file('Planilha padrão -  Tabela de Venda.xlsx'),
                                    sheet_name="Tabela de vendas")
df_cadastro_vendas_0 = pd.read_excel(pasta.get_file('Planilha padrão -  Tabela de Venda.xlsx'),
                                    sheet_name="Cadastro")
# print(df_tabela_vendas)

con = sqlite3.connect("C:\\Users\\kevin.maykel\\PycharmProjects\\City-Web\\db.sqlite3")

df_tabela_vendas_0 = df_tabela_vendas
df_cadastro_vendas = df_cadastro_vendas_0

sqlite_disponiveis = "SELECT * FROM api_disponiveis_tabela_vendas"

df_consulta = pd.read_sql(sqlite_disponiveis, con)
# df_consulta = self.tabela_disponivel()
novos_nomes = [
    'id',
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
df_consulta.columns = novos_nomes
df_consulta.rename(columns={'NomeFantasia':'NOMEFANTASIA_EMP'}, inplace=True)
df_consulta = df_consulta[["Empresa", "Obra", "Unidade", "NOMEFANTASIA_EMP"]]

df_consulta["Empresa"] = df_consulta["Empresa"].astype(str)
df_consulta["Obra"] = df_consulta["Obra"].astype(str)
df_consulta["Unidade"] = df_consulta["Unidade"].astype(str)

df_tabela_vendas_0["Empreendimento"] = df_tabela_vendas_0["Empreendimento"].astype(str)
df_tabela_vendas_0["Obra"] = df_tabela_vendas_0["Obra"].astype(str)
df_tabela_vendas_0["Unidade"] = df_tabela_vendas_0["Unidade"].astype(str)
# print(df_tabela_vendas_0)

df_tabela_vendas = pd.merge(left=df_tabela_vendas_0, right=df_consulta, how="inner", left_on=["Empreendimento", "Obra", "Unidade"], right_on=["Empresa", "Obra", "Unidade"])
# print(df_tabela_vendas)

if 'Excecao' in df_tabela_vendas.columns:
    df_tabela_vendas = df_tabela_vendas[df_tabela_vendas["Excecao"] != "sim"]

df_cadastro_vendas["Empreendimento"] = df_cadastro_vendas["Empreendimento"].astype(str)
df_tabela_vendas["Empreendimento"] = df_tabela_vendas["Empreendimento"].astype(str)
print(df_cadastro_vendas)
df_tabela_vendas = df_tabela_vendas.fillna("NULL")
df_cadastro_vendas = df_cadastro_vendas.fillna("NULL")

json_estrutura = {}
for empreendimento, grupo in df_tabela_vendas.groupby("Empreendimento"):
    unidades = grupo.to_dict(orient="records")

    cadastro_info = df_cadastro_vendas[df_cadastro_vendas["Empreendimento"] == empreendimento]
    cadastro_dict = cadastro_info.to_dict(orient="records")

    json_estrutura[empreendimento] = {
        "Vendas": unidades,
        "Cadastro": cadastro_dict
    }

with open("resultado.json", "w") as f:
    json.dump(json_estrutura, f, indent=4, ensure_ascii=False, default=converter_para_serializavel)
    
    
print(json_estrutura)
