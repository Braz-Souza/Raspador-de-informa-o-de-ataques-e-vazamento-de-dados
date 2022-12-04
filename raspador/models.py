from django.db import models

class Noticia(models.Model):
    link = models.TextField()
    title = models.CharField(max_length=200)
    desc = models.CharField(max_length=200)
    img = models.TextField()