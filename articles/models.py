# ARTICLE models


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import models

from fotoalben.blocks import FotoalbumBlock

import scms2.blocks as scms2blocks
#from scms2.blocks import ImageBlock, ImageAndCitationBlock

from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.wagtailadmin.edit_handlers import  (
    FieldPanel, StreamFieldPanel, MultiFieldPanel, FieldRowPanel
)
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.models import Site
from wagtail.wagtailimages.blocks import ImageChooserBlock




class ArticlePage( Page ):
    subpage_types = []
    anriss = StreamField(
        [
            ('paragraph', scms2blocks.Absatz(
                label = 'Textabsatz'
            )),
            ('fotoalbum', FotoalbumBlock()),
            ('image', scms2blocks.ImageBlock(
                label = 'Bild'
            )),
#            ('image2', ImageChooserBlock(
#                label = 'Bild'
#            )),
        ],
        blank = True,
        null = True
    )
    body = StreamField([
        ('heading', blocks.CharBlock( 
            classname = "full title",
            icon = 'fa fa-header',
            label = 'Überschrift',
            template = 'seiten/blocks/heading.html',
            group = 'Allgemeine Texte'
        )),
        ('paragraph', scms2blocks.Absatz( group = 'Allgemeine Texte')),
#        ('image', ImageChooserBlock()),
        ('image', scms2blocks.ImageBlock(group='Fotos und Bilder')),
        ('img_citation', scms2blocks.ImageAndCitationBlock(group='Fotos und Bilder')),
#        ('fotoalbum', blocks.PageChooserBlock(
#            label='Fotoalbum',
#            target_model='fotoalben.Fotoalbum'
#        ),),
        ('fotoalbum2', FotoalbumBlock(group='Fotos und Bilder' ) ),
        ('bilderliste', scms2blocks.ImgListBlock(label = 'Fotoliste',group='Fotos und Bilder')),
        ('blockquote', scms2blocks.QuoteBlock(group = 'Spezielle Texte')),
        ('komplexe_liste', scms2blocks.ComplexListBlock(group = 'Spezielle Texte')),
        ('video', scms2blocks.YoutubeBlock(group = 'Videos')),
        ('local_video', scms2blocks.LocalVideoBlock(group = 'Videos')),
        ('strophe', scms2blocks.Strophe(group = 'Spezielle Texte')),
        ('video_carousel', scms2blocks.VideoCarouselBlock(group = 'Videos')),
        ('table', TableBlock(
            label = 'Tabelle',
            group = 'Allgemeine Texte'
        )),
    ],
    verbose_name = 'Inhalt')
    datum = models.DateField(
        verbose_name = "angezeigtes Datum der Veröffentlichung",
        blank = True,
        null = True,
        help_text = "Wenn dieses Feld freigelassen wird, wird das aktuelle Datum verwendet (außer, es wird eine spätere Veröffentlichung eingestellt)." 
    )
    enddatum = models.DateField(
        verbose_name = "angezeigtes Enddatum der Veröffentlichung",
        blank = True,
        null = True,
        help_text = "In einigen älteren Artikeln wurde für Berichte über mehrtägige Veranstaltungen der Zeitraum der Veranstaltung als angezeigtes Datum gewählt. Hier kann für solche fälle das Enddatum eingestellt werden." 
    )
    autor = models.CharField(
        max_length = 128,
        blank = True,
        null = True,
        verbose_name = 'Autor des Texts',
        help_text = 'Wenn dieses Feld leer gelassen wird, wirst du als Autor gelistet.' 
    )

    content_panels = Page.content_panels + [
        StreamFieldPanel('anriss'),
        StreamFieldPanel('body'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('datum'),
                FieldPanel('enddatum')
            ])
        ], heading = 'Angezeigtes Datum'),
        FieldPanel('autor')
    ]

    def get_article_date( self ):
        return self.datum or self.go_live_at or self.first_published_at
    class Meta:
        verbose_name = ('Artikel')

class ArticlesIndexPage( Page ):
    icon = "newspaper-o"
    subpage_types = [ 'ArticleContainer' ]
    parent_page_types = [ 'home.HomePage' ]
    def get_icon(self):
        return self.icon
    def get_context(self, request):
        this_site = Site.find_for_request( request )
        context = super(ArticlesIndexPage, self).get_context(request)

        all_articles = ArticlePage.objects.live().order_by('-first_published_at')
        
        site_articles = [
            article for article in all_articles if article.get_site() == this_site 
        ]

        paginator = Paginator(site_articles, 20)

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

        return context
    class Meta:
        verbose_name = ('Artikelliste')

    def get_last_child(self):
        return self.get_children().order_by('path').reverse()[0]
    def get_first_child(self):
        return self.get_children().order_by('path')[0]

    def get_children( self ):
        return super(ArticlesIndexPage, self).get_children().order_by('-slug')

class ArticleContainer( Page ):
    parent_page_types = ['ArticlesIndexPage']
    subpage_types = ['ArticlePage']

    class Meta:
        verbose_name = ('Artikelordner')

    
class ArticleIndexByYearPage( Page ):
    is_creatable = False
