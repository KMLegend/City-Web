#!/bin/bash

set -e  # encerra em caso de erro

echo "Ativando ambiente virtual..."
source env/bin/activate

echo "Executando script Python..."
python Rotinas/atualizacao_bd_sqlite_tb_disponiveis.py

echo "Reiniciando o nginx..."
sudo systemctl restart nginx

echo "Script concluído com sucesso."