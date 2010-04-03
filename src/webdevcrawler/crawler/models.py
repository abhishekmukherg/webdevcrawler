from django.db import models

class Url(models.Model):
    href = models.URLField(verify_exists=True)
    excluded = models.BooleanField(default=False)

    def __unicode__(self):
        return unicode(self.href)

    class Meta:
        app_label = 'crawler'

class Keyword(models.Model):
    word = models.CharField(max_length=128)
    urls = models.ManyToManyField(Url)

    def __unicode__(self):
        return unicode(self.word)

    class Meta:
        app_label = 'crawler'
