from django.db import models


class Disponiveis_tabela_vendas(models.Model):
    produto = models.IntegerField(default=0)
    empresa = models.IntegerField(default=0)
    nome_fantasia = models.CharField(max_length=150, default='')
    obra = models.CharField(max_length=10, default='')
    unidade = models.CharField(max_length=100, default='')
    tipo = models.CharField(max_length=60, default='')
    cod_tipologia = models.IntegerField(default=0)
    tipologia = models.CharField(max_length=60, default='')
    status = models.CharField(max_length=100, default='')
    # data_insercao = models.DateTimeField()

    def __str__(self):
        return f'{self.produto}, {self.empresa}, {self.nome_fantasia}, {self.obra}, {self.unidade}, {self.tipo}, {self.cod_tipologia}, {self.tipologia}, {self.status}, {self.data_insercao}'



# class Tabela_de_vendas(models.Model):
#     empreendimento = models.IntegerField(default=0)
#     obra = models.CharField(max_length=10, default='')
#     unidade = models.CharField(max_length=10, default='')
#     tipo = models.CharField(max_length=60, default='')
#     suites = models.CharField(max_length=10, default='')
#     area_privativa_total = models.FloatField(default=0.0)
#     area_apartamento = models.FloatField(default=0.0)
#     area_descoberta = models.FloatField(default=0.0)
#     area_varanda_coberta = models.FloatField(default=0.0)
#     vagas_garagem = models.CharField(max_length=100)
#     pvto_vagas = models.CharField(max_length=100)
#     esc_garagem = models.CharField(max_length=10)
#     area_esc = models.FloatField(default=0.0)
#     esc_pavimentos = models.CharField(max_length=20)
#     area_esc_pavimentos = models.FloatField(default=0.0)
#     area_armarios = models.FloatField(default=0.0)
#     valor_total = models.FloatField(default=0.0)


# class Cadastro_vendas(models.Model):


