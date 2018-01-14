from __future__ import absolute_import, unicode_literals

from articles.models import ArticlePage

from datetime import datetime
from dateutil.relativedelta import relativedelta
from dateutil.rrule import rrule, YEARLY, SU

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import models

from termine.models import Termin

from wagtail.wagtailcore.models import Page, Site

class HomePage(Page):
    class Meta:
        verbose_name = 'Startseite'  
    subpage_types = [ 
        'articles.ArticlesIndexPage', 
        'seiten.SeitenIndexPage',
#        'vorstand.Vorstandsseite',
#        'menu.MenuContainer',
        'termine.TerminListe',
        'fotoalben.FotoalbumIndexPage',
    ]
    def get_context( self, request ):
        context = super(HomePage, self).get_context(request)

        this_site = Site.find_for_request( request )

        all_articles = ArticlePage.objects.live().order_by('-datum')

        site_articles = [ article for article in all_articles if article.get_site() == this_site ]

        paginator = Paginator(site_articles, 5)

        page = request.GET.get('page')
        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            articles = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            articles = paginator.page(paginator.num_pages)

        context['articles'] = articles
        context['naechster_termin'] = Termin.get_next( request )
        context['sites'] = Site.objects.order_by('site_name').all()
        
        return context

# Tage bis zum Schützenfest :-)
class DBSPage( Page ):
    class Meta:
        verbose_name = 'Anzeige der Tage bis Schützenfest'
        
    template = 'seiten/dbs_page.html'
    title = None
    slug = 'tbs'

    def get_context( self, request ):
        context = super(DBSPage, self).get_context(request)
        today = datetime.now()
        next = rrule(YEARLY, dtstart = now, byweekday=SU(1), bymonth = 7, count = 10)
        context['next'] = []
        for n in next:
            context.netxt.append(n-relativedelta(days=-1))
        return context
