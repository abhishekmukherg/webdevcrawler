import re

import storm.locals


URL_REGEX = re.compile(r'^https?://.*$')


class Link(storm.locals.Storm):

    __storm_table__ = 'urls'
    id = storm.locals.Int(primary=True)
    href = storm.locals.Unicode()

    def __init__(self, href):
        if not URL_REGEX.match(href):
            raise ValueError('Invalid url')
        self.href = href


class Keyword(storm.locals.Storm):

    __storm_table__ = 'keywords'
    id = storm.locals.Int(primary=True)
    word = storm.locals.Unicode()

    def __init__(self, word):
        self.word = word


class LinkKeyword(storm.locals.Storm):

    __storm_table__ = 'link_keyword'
    __storm_primary__ = 'link_id', 'keyword_id'
    link_id = storm.locals.Int()
    keyword_id = storm.locals.Int()


def create_tables(store):
    store.execute('CREATE TABLE urls '
                  '(id INTEGER NOT NULL PRIMARY KEY, '
                  'href VARCHAR)')
    store.execute('CREATE TABLE keywords '
                  '(id INTEGER NOT NULL PRIMARY KEY, '
                  'word VARCHAR)')
    store.execute('CREATE TABLE link_keyword '
                  '(link_id INTEGER NOT NULL, keyword_id INTEGER NOT NULL, '
                  'PRIMARY KEY(link_id, keyword_id))')
