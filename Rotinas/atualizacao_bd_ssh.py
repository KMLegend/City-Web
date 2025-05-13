import paramiko
import sqlite3
import sys
import os
import json

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
        obra = '0o' + row['Obra'][1:] if row['Obra'].startswith('0') else row['Obra']

        valores = (
        str(row["Produto"]), str(row["Empresa"]), json.dumps(row["NomeFantasia"]),
        json.dumps(obra), json.dumps(row["Unidade"]), json.dumps(row["tipo"]),
        json.dumps(row["cod_tipologia"]), json.dumps(row["tipologia"]), json.dumps(row["status"])
    )

    # Construir a query SQL com os valores formatados corretamente
    sql_insert = f"INSERT INTO api_disponiveis_tabela_vendas (Produto, Empresa, NomeFantasia, Obra, Unidade, tipo, cod_tipologia, tipologia, status) VALUES ({', '.join(valores)})"

    # Criar o comando SSH corretamente escapado
    command = f"""
    python3 -c "import sqlite3; conn = sqlite3.connect('{sqlite_file}'); cursor = conn.cursor(); cursor.execute(\\"{sql_insert}\\"); conn.commit(); conn.close();"
    """

    # Executar o comando via SSH
    stdin, stdout, stderr = ssh.exec_command(command)
    output = stdout.read().decode('utf-8')
    errors = stderr.read().decode('utf-8')

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
