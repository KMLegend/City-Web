import datetime
from time import timezone

from django.db import models


class Perguntas(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("Data de Publicação")
    def __str__(self):
        return self.question_text

    def quando_foi_publicado(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Resposta(models.Model):
    question = models.ForeignKey(Perguntas, on_delete=models.CASCADE)
    resposta_text = models.CharField(max_length=200)
    votos = models.IntegerField(default=0)
    def __str__(self):
        return self.resposta_text
