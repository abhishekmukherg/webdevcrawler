from django.test import TestCase
from webdevcrawler.crawler import helpers
from webdevcrawler.crawler import models

class TestGetOrCreate(TestCase):

    def test_exists(self):
        self.assertEqual(len(models.Url.objects.all()), 0)
        m = models.Url(href='http://www.google.com')
        m.save()
        self.assertEqual(m, 
            helpers._get_or_create(models.Url, href='http://www.google.com'))
        all_urls = models.Url.objects.all()
        self.assertEqual(len(all_urls), 1)

    def test_not_exist_nosave(self):
        self.assertEqual(len(models.Url.objects.all()), 0)
        m = helpers._get_or_create(models.Url, href="http://www.google.com")
        self.assertEqual(m.href, 'http://www.google.com')
        self.assertEqual(len(models.Url.objects.all()), 0)
        m.save()
        self.assertEqual(len(models.Url.objects.all()), 1)
        self.assertEqual(m, models.Url.objects.all()[0])

    def test_not_exist_save(self):
        self.assertEqual(len(models.Url.objects.all()), 0)
        m = helpers._get_or_create(models.Url, save=True,
                href="http://www.google.com")
        self.assertEqual(m.href, 'http://www.google.com')
        self.assertEqual(len(models.Url.objects.all()), 1)
        self.assertEqual(m, models.Url.objects.all()[0])
