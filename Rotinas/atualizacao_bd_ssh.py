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
sqlite_file = "/var/www/City-Web/bd.sqlite3"  # Atualize o caminho

try:
    # Conectar via SSH
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, username=username, password=password)
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
            print("Saída:\n", output)
        if errors:
            print("Erros:\n", errors)

except Exception as e:
    print(f"Erro: {e}")
finally:
    ssh.close()
