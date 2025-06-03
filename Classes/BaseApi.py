import pandas as pd
import json
import pyodbc
import datetime
from shareplum import Site, Office365
from shareplum.site import Version
import sqlite3

from siteCity.settings import BASE_DIR


class Api:
    def __init__(self):
        self.json = None
        self.conn = None
        self.cursor = None

    def conexao_bd_sql_server(self, usuario, senha):
        try:
            dados_conexao = (
                "DSN=MSSQLCONN;"
                f"UID={usuario};"
                f"PWD={senha};"
            )
            self.conn = pyodbc.connect(dados_conexao)
        except pyodbc.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")

        return self.conn

    def tabela_disponivel(self):
        conn = self.conexao_bd_sql_server(usuario="usruau", senha="spfmed4$")
        sql = """
            SELECT
                    TotalPerson.prod_unid AS  Produto,
                    TotalPerson.empresa_unid AS  Empresa,
                    TotalPerson.NomeFantasia_emp  AS NomeFantasia,
                    TotalPerson.obra_unid AS  Obra,
                    UPPER(TotalPerson.identificador_unid) AS Unidade,
                    CASE
                        WHEN UPPER(TotalPerson.identificador_unid) LIKE 'A%' THEN 'ALMOXERIFADO'
                        WHEN UPPER(TotalPerson.identificador_unid) LIKE 'E%' THEN 'ESCANINHOS'
                        WHEN UPPER(TotalPerson.identificador_unid) LIKE 'L%' THEN 'LOJAS'
                        WHEN UPPER(TotalPerson.identificador_unid) LIKE 'V%' THEN 'VAGA VEICULOS'
                        WHEN UPPER(TotalPerson.identificador_unid) LIKE 'G%' THEN 'VAGA VEICULOS'
                        WHEN UPPER(TotalPerson.identificador_unid) LIKE 'M%' THEN 'VAGA MOTOS'
                        WHEN UPPER(TotalPerson.identificador_unid) LIKE '%MT' THEN 'VAGA MOTOS'
                        WHEN TotalPerson.empresa_unid IN (76) THEN 'SALA COMERCIAL'
                        WHEN TotalPerson.empresa_unid IN (58,75,96,98,106) THEN 'LOTE RESIDENCIAL'
                    ELSE 'APARTAMENTO RESIDENCIAL' END  AS  Tipo,
                    TotalPerson.codtipprod_unid AS Cod_Tipologia,
                    TotalPerson.descricao_tipprod AS  Tipologia,
                    UPPER(TotalPerson.Descr_status) AS Status
            FROM (
                SELECT
                    UP.prod_unid,
                    UP.empresa_unid,
                    CASE
                        WHEN UP.empresa_unid = 42 AND UP.obra_unid LIKE '2T%' THEN 'CITY PARK PALACE'
                        WHEN UP.empresa_unid = 42 AND UP.obra_unid LIKE '3T%' THEN 'CITY PARK ROYAL'
                        WHEN UP.empresa_unid = 42 AND UP.obra_unid LIKE '420%' THEN 'CITY PARK MAJESTIC'
                    ELSE E.NomeFantasia_emp END AS NomeFantasia_emp,
                    UP.obra_unid,
                    --O.descr_obr,
                    UP.identificador_unid,
                    UP.codtipprod_unid,
                    TP.descricao_tipprod,
                    CASE
                        WHEN UP.vendido_unid = 0 THEN 'Disponível'
                        WHEN UP.vendido_unid = 1 THEN
                            (CASE WHEN UD.tipocontrato_udt IN( 1, 2, 5 ) THEN 'Locada' ELSE 'Vendida' END)
                        WHEN UP.vendido_unid = 2 THEN 'Reservado'
                        WHEN UP.vendido_unid = 3 THEN 'Proposta'
                        WHEN UP.vendido_unid = 4 THEN 'Quitado'
                        WHEN UP.vendido_unid = 5 THEN 'Escriturado'
                        WHEN UP.vendido_unid = 6 THEN 'Em venda'
                        WHEN UP.vendido_unid = 7 THEN 'Suspenso'
                        WHEN UP.vendido_unid = 8 THEN 'Fora de venda'
                        WHEN UP.vendido_unid = 9 THEN 'Em acerto'
                        WHEN UP.vendido_unid = 10 THEN 'Dação' END AS Descr_status
                FROM  UAU.dbo.UnidadePer AS UP
            
                LEFT JOIN UAU.dbo.UnidadeDetalhe AS UD
                    ON UP.empresa_unid = UD.empresa_udt
                    AND UP.prod_unid = UD.prod_udt
                    AND UP.numper_unid = UD.numper_udt
            
                LEFT JOIN UAU.dbo.tipologiaproducao AS TP
                    ON TP.codigo_tipprod = UP.codtipprod_unid
            
                LEFT JOIN UAU.dbo.Empresas AS E
                ON UP.empresa_unid = E.Codigo_emp
            
                LEFT JOIN UAU.dbo.Obras AS O
                ON UP.obra_unid = O.cod_obr
                AND UP.empresa_unid = O.Empresa_obr
            
            
            )  AS TotalPerson
            
            WHERE TotalPerson.prod_unid NOT IN (36,58,65)
                AND TotalPerson.empresa_unid NOT IN (9,19,78)
                AND (TotalPerson.identificador_unid IS NOT NULL
                AND TotalPerson.identificador_unid NOT LIKE '')
                AND TotalPerson.Descr_status = 'DISPONÍVEL'
                AND TotalPerson.obra_unid LIKE '%I'
        """
        df_consulta = pd.read_sql(sql, conn)
        conn.close()
        return df_consulta

    def conexao_bd_sqlite(self):
        self.con = sqlite3.connect(BASE_DIR / "db.sqlite3")
        return self.con

    def insere_tabela_disponivel_sqlite(self):
        df_consulta = self.tabela_disponivel()
        con = self.conexao_bd_sqlite()
        try:
            sql_insert = ""
        except Exception as e:
            print(e)

    def deleta_tabela_disponivel_sqlite(self):
        con = self.conexao_bd_sqlite()

    def tabela_disponivel_sqlite(self):
        con = self.conexao_bd_sqlite()
        sql = "SELECT * FROM api_disponiveis_tabela_vendas"
        df = pd.read_sql(sql, con)
        return df

    def tabela_de_vendas_sharepoint(self, nome_planilha):
        authcookie = Office365('https://cityinc123.sharepoint.com', username='inovacao.sistemas@cityinc.com.br',
                               password='Zat41304').GetCookies()
        site = Site('https://cityinc123.sharepoint.com/inovacao-sistemas/', version=Version.v365, authcookie=authcookie)

        pasta = site.Folder('Documentos Compartilhados/Compartilhado/Comercial')
        df_tabela_vendas = pd.read_excel(pasta.get_file('Planilha padrão -  Tabela de Venda.xlsx'),
                                           sheet_name=nome_planilha)

        return df_tabela_vendas

    def tabela_vendas_sqlite(self):
        con = self.conexao_bd_sqlite()
        cur = con.cursor()
        df_consulta = self.tabela_de_vendas_sharepoint("Tabela de vendas")
        print(df_consulta.columns)
        truncate = """
        DROP TABLE tabelaDeVendas;
        """
        sql_create = """
        CREATE TABLE tabelaDeVendas (
            Empreendimento  int,
            Obra  varchar(255),
            Unidade  varchar(255),
            Tipo  varchar(255),
            Suites  int,
            Area Privativa Total (m2)  float,
            Area Apart. (m2)  float,
            Area descoberta (m2)  float,
            Area Varanda Coberta (m²) float,
            Vagas de Garagem  varchar(255),
            PVTO VAGAS  varchar(255),
            ESC. GAR.  varchar(255),
            Area ESC.  float,
            ESC. PAV.  varchar(255),
            Area ESC. PAV.  int,
            Valor Total  float,
            Sinal  float,
            Sinal 3 parcelas  float,
            Mensais  float,
            Semestrais  float,
            Anual  float,
            SUBTOTAL  float,
            FINANCIAMENTO BANCARIO  float,
            Tipologia  varchar(255),
            STATUS  varchar(255),
        );
        """

        cur.execute(truncate)
        cur.execute(sql_create)

        for index, row in df_consulta.iterrows():
            print(row)
            sql_insert = f"""

            INSERT INTO tabelaDeVendas VALUES ('{row['Empreendimento']}','{row['Obra']}','{row['Unidade']}','{row['Tipo']}','{row['Suites']}','{row['Area Privativa Total (m2)']}','{row['Area Apart. (m2)']}','{row['Area descoberta (m2)']}','{row['Vagas de Garagem']}','{row['PVTO VAGAS']}','{row['ESC. GAR.']}','{row['Area ESC.']}','{row['ESC. PAV.']}','{row['Area ESC. PAV.']}','{row['Valor Total']}','{row['Sinal']}','{row['Sinal 3 parcelas']}','{row['Mensais']}','{row['Semestrais']}','{row['Anual']}','{row['SUBTOTAL']}','{row['FINANCIAMENTO BANCARIO']}','{row['Tipologia']}','{row['STATUS']}')

            """

            cur.execute(sql_insert)

        con.commit()


    def converter_para_serializavel(self, obj):
        if isinstance(obj, pd.Timestamp):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()
        raise TypeError(f"Tipo não serializável: {type(obj)}")

    def dadosApi(self):

        con = self.conexao_bd_sqlite()

        # sql_tabela_de_vendas = "SELECT * FROM tabelaDeVendas"

        df_tabela_vendas_0 = self.tabela_de_vendas_sharepoint("Tabela de vendas")
        df_cadastro_vendas = self.tabela_de_vendas_sharepoint("Cadastro")

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

        df_tabela_vendas = pd.merge(left=df_tabela_vendas_0, right=df_consulta, how="inner", left_on=["Empreendimento", "Obra", "Unidade"], right_on=["Empresa", "Obra", "Unidade"])
        print(df_tabela_vendas)

        if 'Excecao' in df_tabela_vendas.columns:
            df_tabela_vendas = df_tabela_vendas[df_tabela_vendas["Excecao"] != "sim"]

        df_cadastro_vendas["Empreendimento"] = df_cadastro_vendas["Empreendimento"].astype(str)
        df_tabela_vendas["Empreendimento"] = df_tabela_vendas["Empreendimento"].astype(str)

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
            json.dump(json_estrutura, f, indent=4, ensure_ascii=False, default=self.converter_para_serializavel)

        return json_estrutura