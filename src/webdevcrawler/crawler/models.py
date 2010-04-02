from django.db import models

class Url(models.Model):
    href = models.CharField(max_length=512)
    excluded = models.BooleanField(default=False)

class Keyword(models.Model):
    word = models.CharField(max_length=128)
    urls = models.ManyToManyField(Url)
