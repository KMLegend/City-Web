# Generated by Django 5.1.3 on 2024-12-05 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_remove_disponiveis_tabela_vendas_data_insercao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='disponiveis_tabela_vendas',
            name='nome_fantasia',
            field=models.CharField(default='', max_length=150),
        ),
    ]
