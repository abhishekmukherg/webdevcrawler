from django.db import models

class Url(models.Model):
    href = models.URLField(verify_exists=True)
    excluded = models.BooleanField(default=False)

class Keyword(models.Model):
    word = models.CharField(max_length=128)
    urls = models.ManyToManyField(Url)
