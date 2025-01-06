import paramiko
import sqlite3
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Classes.BaseApi import Api

api = Api()
# Configuração de conexão SSH
hostname = "46.202.149.159"
username = "root"
password = "G@E99X?/g~rAAh>@f7$b"  # Substitua pela senha correta

# Caminho do banco de dados no servidor
sqlite_file = "/var/www/City-Web/db.sqlite3"  # Atualize o caminho

def insert(ssh):
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

    # Convertendo valores nulos para texto padrão ou zero
    dados.fillna('', inplace=True)

    # Iterando por cada linha do DataFrame
    for _, row in dados.iterrows():
        # row['obra'] = row['Obra'].strip
        if row['Obra'].startswith('0'):  # Verifica se começa com 0 e é um número
            obra = '0o' + row['Obra'][1:]
            print("entrou")
        else:
            obra = row['Obra']

        # Construir comando SQL escapado
        sql_insert = f"""INSERT INTO api_disponiveis_tabela_vendas (Produto, Empresa, NomeFantasia, Obra, Unidade, tipo, cod_tipologia, tipologia, status) VALUES ("{row["Produto"]}","{row["Empresa"]}","{row["NomeFantasia"]}","{row["Obra"]}","{row["Unidade"]}","{row["tipo"]}","{row["cod_tipologia"]}","{row["tipologia"]}","{row["status"]}")"""

        command = f"""
        python3 -c "import sqlite3; conn = sqlite3.connect('{sqlite_file}'); cursor = conn.cursor(); cursor.execute('{sql_insert}'); conn.commit(); conn.close();"
        """

        # Executar comando via SSH
        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.read().decode('utf-8')
        errors = stderr.read().decode('utf-8')

        # Exibir resultados
        if output:
            print("Saída INSERT:\n", output)
        if errors:
            print("Erros INSERT:\n", errors)
def delete(ssh):
    df = api.tabela_disponivel_sqlite()
    # print(df)
    for _, row in df.iterrows():
        data = {
            'id': row['id']
        }
        query = f"DELETE FROM api_disponiveis_tabela_vendas WHERE id = {row['id']}"

        # Configurar sessão remota para Python
        command = f"""
            python3 -c "import sqlite3; \
            conn = sqlite3.connect('{sqlite_file}'); \
            cursor = conn.cursor(); \
            cursor.execute('{query}'); \
            conn.commit(); \
            print('Comando executado com sucesso!'); \
            conn.close();"
                """

        # Executar comando
        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.read().decode('utf-8')
        errors = stderr.read().decode('utf-8')

        # Exibir resultados
        if output:
            print("Saída DELETE:\n", output)
        if errors:
            print("Erros DELETE:\n", errors)
try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, username=username, password=password)

    # delete(ssh)
    insert(ssh)

except Exception as e:
    print(f"Erro: {e}")
finally:
    ssh.close()
