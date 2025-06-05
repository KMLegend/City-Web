#!/bin/bash

echo "Ativando VPN..."
sudo openvpn --config /etc/openvpn/client/Hostinger_-_ubuntu-config.ovpn --daemon

# Aguarda VPN estabelecer, verificando porta 1433 no servidor SQL
echo "Aguardando VPN conectar ao banco de dados..."

MAX_TRIES=12  # aguardar no máximo 60s (12 tentativas x 5s)
TRY=0

until nc -z -w2 192.168.100.250 1433 || [ $TRY -ge $MAX_TRIES ]; do
    echo "Tentativa $((TRY+1)) de conexão com 192.168.100.250:1433..."
    TRY=$((TRY+1))
    sleep 5
done

if [ $TRY -ge $MAX_TRIES ]; then
    echo "❌ Falha ao conectar ao banco de dados via VPN. Abortando script."
    exit 1
fi

echo "✅ Conexão VPN e banco detectada. Continuando..."

echo "Ativando ambiente virtual..."
source /var/www/City-Web/env/bin/activate

echo "Executando script Python..."
python /var/www/City-Web/Rotinas/atualizacao_bd_sqlite_tb_disponiveis.py

echo "Reiniciando NGINX..."
sudo service nginx restart

