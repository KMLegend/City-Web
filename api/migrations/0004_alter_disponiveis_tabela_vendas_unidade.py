# Generated by Django 5.1.3 on 2024-12-05 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_disponiveis_tabela_vendas_nome_fantasia'),
    ]

    operations = [
        migrations.AlterField(
            model_name='disponiveis_tabela_vendas',
            name='unidade',
            field=models.CharField(default='', max_length=100),
        ),
    ]
