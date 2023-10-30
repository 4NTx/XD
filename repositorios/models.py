from django.db import models

class Estudante(models.Model):
    nome = models.CharField(max_length=255)
    identificador_github = models.CharField(max_length=255, null=True, blank=True)

class Repositorio(models.Model):
    nome = models.CharField(max_length=255)
    estudante = models.ForeignKey(Estudante, on_delete=models.CASCADE)
