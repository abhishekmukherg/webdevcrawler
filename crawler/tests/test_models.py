import unittest

import storm.locals

import webcrawler.models


class DatabaseTest(unittest.TestCase):

    def setUp(self):
        self.db = storm.locals.create_database('sqlite:')
        self.store = storm.locals.Store(self.db)
        webcrawler.models.create_tables(self.store)

    def tearDown(self):
        del self.db
        del self.store
        import gc
        gc.collect()


class TestKeyword(DatabaseTest):

    def test_create(self):
        kw = self.store.add(webcrawler.models.Keyword(u"wordz"))
        self.store.flush()
        self.assertEqual(u'wordz', unicode(kw.word))


class TestLink(DatabaseTest):

    def test_create_fail(self):
        self.assertRaises(ValueError, webcrawler.models.Link, 'foo')

    def test_create(self):
        link = self.store.add(
                webcrawler.models.Link(u"http://www.google.com"))
        self.store.flush()
        self.assertEqual(u'http://www.google.com', unicode(link.href))
