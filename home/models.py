from __future__ import absolute_import, unicode_literals

from articles.models import ArticlePage

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

