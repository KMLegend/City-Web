#!/bin/bash


echo "Ativando ambiente virtual..."
source /var/www/City-Web/env/bin/activate

echo "Executando script Python..."
python /var/www/City-Web/Rotinas/atualizacao_bd_sqlite_tb_disponiveis.py

echo "Reiniciando NGINX..."
sudo service nginx restart

