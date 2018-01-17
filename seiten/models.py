from .blocks import TOCBlock
from django.db import models
from django.utils.text import slugify

from fotoalben.blocks import FotoalbumBlock

from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailadmin.edit_handlers import FieldPanel, \
    StreamFieldPanel, InlinePanel, PageChooserPanel, \
    MultiFieldPanel
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtaildocs.blocks import DocumentChooserBlock
from wagtail.wagtailembeds.blocks import EmbedBlock


import scms2.blocks as scms2blocks

# Create your models here.


    
class LinkSeiteField( models.Model ):
    link_page = models.ForeignKey(
        'wagtailcore.Page',
        null = True,
        blank = True,
        related_name = '+'
    )
    @property
    def link(self):
        return self.link_page.url


    panels = [
        PageChooserPanel( 'link_page' )
    ]
    class Meta:
        abstract = True

class VerlinkteSeiten( LinkSeiteField ):
    panels = [
        MultiFieldPanel( LinkSeiteField.panels, "Link"),
    ]

    class Meta:
        abstract = True



class Seite( Page ):
    subpage_types = ['fotoalben.Fotoalbum', 'seiten.Seite', 'fotoalben.FotoalbumIndexPage']
    parent_page_types = [ 'seiten.SeitenIndexPage', 'seiten.Seite' ]
    kurztitel = models.CharField(
        max_length = 64,
        null = True,
        blank = True,
        help_text = 'Kurzer Titel, der in Menus benutzt wird'
    )
    body = StreamField(
        [
            # Simple Textbausteine
            ('heading', scms2blocks.HeadingBlock( 
                classname = "full title",group = 'Einfacher Text'
            )),
            ('paragraph', scms2blocks.Absatz(group = 'Einfacher Text')),
            ('table', TableBlock(label = 'Tabelle',group = 'Einfacher Text')),

            # Fotos und Bilder
            ('image', scms2blocks.ImageBlock(group = 'Fotos und Bilder')),
            ('album', FotoalbumBlock(group = 'Fotos und Bilder')),
            ('bilderliste', scms2blocks.ImgListBlock(label = 'Fotoliste',group = 'Fotos und Bilder')),
            ('img_citation', scms2blocks.ImageAndCitationBlock(group = 'Fotos und Bilder')),
            
            # spezieller text
            ('quote', scms2blocks.QuoteBlock(group = 'Spezieller Text')),
            ('komplexe_liste', scms2blocks.ComplexListBlock(group = 'Spezieller Text')),
            ('strophe', scms2blocks.Strophe(group = 'Spezieller Text')),
            ('adresse', scms2blocks.Adresse(group = 'Spezieller Text')),

            # Videos
            ('youtube_video', EmbedBlock(group = 'Videos')),
            ('local_video', scms2blocks.LocalVideoBlock(group = 'Videos')),
            ('video_karussell', scms2blocks.VideoCarouselBlock(group = 'Videos')),

            # Spezieller Inhalt

            ('map', scms2blocks.OpenStreetMapBlock(group = 'spezielle Inhalte')),
            ('sitemap',scms2blocks.SitemapBlock(group = 'spezielle Inhalte')),
            ('toc',TOCBlock(group = 'spezielle Inhalte')),
        ],
        verbose_name = 'Seiteninhalt'
    )
    
    content_panels = Page.content_panels + [
        FieldPanel('kurztitel'),
        StreamFieldPanel('body'),
    ]

    def get_context( self, request ):
        context = super(Seite, self).get_context(request)
        headings = []
        heading_names = []
        has_toc = False
        for block in self.body:
            if block.block_type == 'toc':
                has_toc = True
            if block.block_type == 'heading':
                headings.append(block.value)
        context['has_toc'] = has_toc
        context['headings'] = headings
        return context

class SeitenIndexPage( Page ):
    subpage_types = ['seiten.Seite']

    def get_context( self, request ):
        context = super(SeitenIndexPage, self).get_context(request)
        context['children'] = self.get_children().live()
        return context
    class Meta:
        verbose_name = 'Ordner für Unterseiten'
