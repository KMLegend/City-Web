# Generated by Django 5.1.3 on 2024-12-11 13:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_alter_disponiveis_tabela_vendas_empresa_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='disponiveis_tabela_vendas',
            old_name='Produto',
            new_name='Produt',
        ),
    ]
