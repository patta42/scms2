'''
Script to import data from the old website to wagtail.

Has to do some compromises since images are not on the same
location as before. This has to be done manually. 
Tables might also be a problem, I'll check that later.

The idea is to store the html in a paragraph-StreamField in the body
element (same for introduction).
'''

import psycopg2 as pg

from django.core.management.base import BaseCommand, CommandError
from articles.models import ArtikelPage

SCHEMAS = ['bruderschaft','dinschede','gloesingen','oeventrop','ssg']

PARENTS = {
    'dinschede' : 6,
}


class DBObj():
    def __init__(self, cursor, row):
        for (attr, val) in zip((d[0] for d in cursor.description), row) :
            setattr(self, attr, val)

def connect2scms():
    conn = pg.connect('dbname=scms user=patta')
    return conn.cursor()


class Command(BaseCommand):
    what = "artikel"
    def __init__( self , *args, **kwargs):
        self.cur = connect2scms()
 
        super(Command, self).__init__(*args, **kwargs)

    def handle( self, *args, **options):
        schema = options['schema']
        if schema not in PARENTS.keys():
            raise CommandError('Cannot import from "%s"' % options['schema'])
        parent = ArtikelPage.objects.get(pk = PARENTS[schema])
        cur = connect2scms
        
        cur.execute("SELECT * FROM {}.{};".format(schema,what))

        for content in cur:
            obj = DBObj(cur, content)
            print("id: {}, Jahr: {}".format(obj.id,obj.erstelldatum.year))
        

