import pandas as pd
import json
import pyodbc
import datetime
from shareplum import Site, Office365
from shareplum.site import Version


class Api:
    def __init__(self):
        self.json = None
        self.conn = None
        self.cursor = None

    def conexao_bd(self, usuario, senha, database):
        try:
            dados_conexao = (
                "Driver={SQL Server};"
                "Server=srv-sql01;"
                f"Database={database};"
                f"UID={usuario};"
                f"PWD={senha};"
            )
            self.conn = pyodbc.connect(dados_conexao)
        except pyodbc.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")

        return self.conn

    def tabelaDisponivel(self):
        conn = self.conexao_bd(usuario="usruau", senha="spfmed4$", database="BI")
        sql = """
                SELECT 
                    BASE."Produto" ,
                    BASE."Empresa" ,
                    BASE."Obra" ,
                    BASE."Unidade" ,
                    BASE."Tipo" ,
                    BASE."Cod_Tipologia" ,
                    BASE."Tipologia" ,
                    BASE."Status" 
                FROM (
                    SELECT DISTINCT
                        "prod_unid" AS  "Produto",
                        "empresa_unid" AS  "Empresa",
                        "obra_unid" AS  "Obra",
                        UPPER("identificador_unid") AS "Unidade" ,
                        CASE 
                            WHEN UPPER("identificador_unid") LIKE 'A%' THEN 'ALMOXERIFADO'
                            WHEN UPPER("identificador_unid") LIKE 'E%' THEN 'ESCANINHOS'
                            WHEN UPPER("identificador_unid") LIKE 'L%' THEN 'LOJAS'
                            WHEN UPPER("identificador_unid") LIKE 'V%' THEN 'VAGA VEICULOS'
                            WHEN UPPER("identificador_unid") LIKE 'G%' THEN 'VAGA VEICULOS'
                            WHEN UPPER("identificador_unid") LIKE 'M%' THEN 'VAGA MOTOS'
                            WHEN UPPER("identificador_unid") LIKE '%MT' THEN 'VAGA MOTOS'
                            WHEN "empresa_unid" IN (76) THEN 'SALA COMERCIAL'
                            WHEN "empresa_unid" IN (58,	75,	96,	98,	106) THEN 'LOTE RESIDENCIAL'
                        ELSE 'APARTAMENTO RESIDENCIAL' END  AS  "Tipo",
                        "codtipprod_unid" AS  "Cod_Tipologia" ,
                        "descricao_tipprod" AS  "Tipologia" ,
                        UPPER("descr_status") AS "Status"

                    FROM BI.dbo.TB_GER_CONTROLE_ESTOQUE_VSO
                    WHERE "prod_unid" NOT IN (36,58,65) 
                        AND "empresa_unid" NOT IN (9,19,78) 
                        AND (UPPER("identificador_unid") IS NOT NULL 
                        AND UPPER("identificador_unid") NOT LIKE '')

                ) AS BASE

                WHERE BASE."Status" = 'DISPONÍVEL'
                AND BASE."Obra" LIKE '%I'
                """
        df_consulta = pd.read_sql(sql, conn)
        conn.close()
        return df_consulta

    def converter_para_serializavel(self, obj):
        if isinstance(obj, pd.Timestamp):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()
        raise TypeError(f"Tipo não serializável: {type(obj)}")

    def dadosApi(self):

        authcookie = Office365('https://cityinc123.sharepoint.com', username='inovacao.sistemas@cityinc.com.br',
                               password='Zat41304').GetCookies()
        site = Site('https://cityinc123.sharepoint.com/inovacao-sistemas/', version=Version.v365, authcookie=authcookie)

        pasta = site.Folder('Documentos Compartilhados/Compartilhado/Comercial')

        df_consulta = self.tabelaDisponivel()
        df_consulta = df_consulta[["Empresa", "Obra", "Unidade"]]

        df_tabela_vendas_0 = pd.read_excel(pasta.get_file('Planilha padrão -  Tabela de Venda.xlsx'), sheet_name="Tabela de vendas")
        df_cadastro_vendas = pd.read_excel(pasta.get_file('Planilha padrão -  Tabela de Venda.xlsx'), sheet_name="Cadastro")

        df_tabela_vendas_0["Empreendimento"] = df_tabela_vendas_0["Empreendimento"].astype(str)
        df_consulta["Empresa"] = df_consulta["Empresa"].astype(str)

        df_tabela_vendas_0["Obra"] = df_tabela_vendas_0["Obra"].astype(str)
        df_consulta["Obra"] = df_consulta["Obra"].astype(str)

        df_tabela_vendas_0["Unidade"] = df_tabela_vendas_0["Unidade"].astype(str)
        df_consulta["Unidade"] = df_consulta["Unidade"].astype(str)

        df_tabela_vendas = pd.merge(left=df_tabela_vendas_0, right=df_consulta, how="inner", left_on=["Empreendimento", "Obra", "Unidade"], right_on=["Empresa", "Obra", "Unidade"])

        df_cadastro_vendas["Empreendimento"] = df_cadastro_vendas["Empreendimento"].astype(str)
        df_tabela_vendas["Empreendimento"] = df_tabela_vendas["Empreendimento"].astype(str)

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
            json.dump(json_estrutura, f, indent=4, ensure_ascii=False, default=self.converter_para_serializavel)

        return json_estrutura
        # return df_tabela_vendas