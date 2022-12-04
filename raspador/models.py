from django.db import models

class Noticia(models.Model):
    link = models.TextField()
    img = models.TextField()
    title = models.CharField(max_length=200)
    desc = models.CharField(max_length=200)