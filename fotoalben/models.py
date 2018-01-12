from .edit_handlers import InlineImagePanel

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import models
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.template.loader import render_to_string

from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey, ParentalManyToManyField

from taggit.models import TaggedItemBase, Tag

from wagtail.contrib.wagtailroutablepage.models import RoutablePageMixin, route
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, MultiFieldPanel, InlinePanel
)
from wagtail.wagtailcore.models import (
    Page, Orderable, Collection, Site
)
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel


class ImageLink( models.Model ):
    '''
    Model to link to an image
    '''

    linked_image = models.ForeignKey(
        'wagtailimages.Image',
        blank = True,
        null = True,
        on_delete = models.SET_NULL,
        related_name = '+',
        verbose_name = 'enthaltenes Bild',
    )
    promote = models.BooleanField(
        default = False,
        verbose_name= 'Dieses Bild als Titelbild verwenden'
    )
    panels = [
        ImageChooserPanel('linked_image'),
        FieldPanel('promote')
    ]
    class Meta:
        abstract = True

class LinkedImages( ImageLink ):
    class Meta: 
        abstract = True
        
    panels = [
        MultiFieldPanel( ImageLink.panels, "Bild"),
    ]

class FotoalbumImages( Orderable, LinkedImages ):
    images = ParentalKey( 'fotoalben.Fotoalbum', related_name = 'verlinkte_bilder' )

class FotoalbumTag(TaggedItemBase):
    content_object = ParentalKey('Fotoalbum', related_name='tagged_items')

class Fotoalbum( RoutablePageMixin, Page ):
    parent_page_types = ['fotoalben.FotoalbumCollection','seiten.Seite' ]
    subpage_types = []
    einleitung = models.TextField(
        max_length = 512,
        blank = True,
        null = True
    )
    collection = models.ForeignKey(
        Collection,
        null = True,
        blank = True,
        on_delete = models.SET_NULL
    )
    # autor = models.CharField(
    #     max_length = 128,
    #     blank = True,
    #     null = True,
    #     verbose_name = 'Autor des Texts',
    #     help_text = 'Wenn dieses Feld leer gelassen wird, wirst du als Autor gelistet.' 
    # )
    datum = models.DateField(
        verbose_name = "angezeigtes Datum der Veröffentlichung",
        blank = True,
        null = True,
        help_text = "Wenn dieses Feld freigelassen wird, wird das aktuelle Datum verwendet (außer, es wird eine spätere Veröffentlichung eingestellt)." 
    )

    tags = ClusterTaggableManager(through=FotoalbumTag, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('tags'),
        FieldPanel('einleitung'),
        InlineImagePanel('verlinkte_bilder', label = "Bilder"),
        FieldPanel('datum'),
#        FieldPanel('autor')
    ]
    settings_panels = Page.settings_panels + [
        FieldPanel('collection')
    ]
    
    def get_tags(self):
        """
        Stolen from bakerydemo
        """
        tags = self.tags.all()
        return tags

    def get_parent_containers( self ):
        return Page.objects.ancestor_of( self ).descendant_of( self.get_site().root_page)

    def get_neighbors( self ):
        return Fotoalbum.objects.sibling_of(self, inclusive = False)

    @route(r'^$')
    def base( self, request ):
        return TemplateResponse(
            request,
            self.get_template(request),
            self.get_context(request)
        )




    @route(r'^(\d+)/$')
    def pic_by_id( self, request, id_ ):
        return TemplateResponse(
            request,
            'fotoalben/pic_by_id.html',
            self.get_single_pic_context(request, id_ )
        )
        
    def get_single_pic_context( self, request, id_ ):
        id_ = int(id_)
        images = self.verlinkte_bilder.all()
        
        image = None
        for img in images:
            if img.id == id_:
                image = img;
                break;
        try:
            prev = images.filter(sort_order = image.sort_order - 1)[0]
        except:
            prev = None
        try:
            nxt = images.filter(sort_order = image.sort_order + 1)[0]
        except:
            nxt = None
        context = super( Fotoalbum, self ).get_context( request )
        context['image'] = image
        context['prev'] = prev
        context['next'] = nxt
        context['n_images'] = len(images)

        return context
    
    def get_context( self, request ):
        
        ppp = 5 # pics per page
        context = super( Fotoalbum, self ).get_context( request )
        bilder = self.verlinkte_bilder.all()
        paginator = Paginator(bilder, ppp)
        if len(bilder) % ppp == 0:
            sections = [
                paginator.page(sec + 1) for sec in range(len(bilder)//ppp )
            ]
        else:
            sections = [
                paginator.page(sec + 1) for sec in range(len(bilder)//ppp + 1)
            ]
        context['sections'] = sections
        context['bilder'] = bilder
        return context

    def get_head_image( self ):
        if self.verlinkte_bilder.all().filter(promote = True).exists():
            ret = self.verlinkte_bilder.all().filter(promote = True).first().linked_image
        else:
            ret = self.verlinkte_bilder.all().first().linked_image

        return ret

    def render_as_child( self, depth = -1 ):
        return render_to_string(
            'fotoalben/fotoalbum_as_child.html',
            { 
                "page" : self, 
                "depth" : depth+1
            }
        )

class FotoalbumCollection( Page ):
    class Meta:
        verbose_name = 'Sammlung von Fotoalben'

    subpage_types = ['fotoalben.Fotoalbum', 'fotoalben.FotoalbumCollection']

    def render_as_child ( self, depth = -1 ):
        return render_to_string(
            'fotoalben/collection_as_child.html',
            { "page" : self, "depth" : depth+1 }
        )

    def get_fotoalben( self ):
        return Fotoalbum.objects.descendant_of(self).live()

    def get_num_pics ( self ):
        num = 0;
        for album in self.get_fotoalben():
            num += album.specific.verlinkte_bilder.count()
        return num

    def get_num_albums( self ):
        return self.get_fotoalben().count()

    def get_collections( self ):
        return FotoalbumCollection.objects.descendant_of(self).live()

    def get_num_collections( self ):
        return self.get_collections().count()
    

class FotoalbumIndexPage( RoutablePageMixin, Page ):
    icon = "picture-o"
    subpage_types = ['fotoalben.FotoalbumCollection']

    sort = models.BooleanField(
        default = True,
        verbose_name = 'Inhalte sortieren?',
        help_text = 'Die Inhalte werden absteigend alphabetisch sortiert. Sonnvoll für Jahreszahlen mit neuesten Jahren zuerst.'
    )

    content_panels = Page.content_panels + [
        FieldPanel('sort'),
    ]

    def get_icon(self):
        return self.icon
    def get_last_child( self ):
        return self.get_children().order_by('path').reverse()[0]
    def get_first_child( self ):
        return self.get_children().order_by('path')[0]
    def get_children( self ):
        children = super(FotoalbumIndexPage, self).get_children()
        if self.sort:
            return children.order_by('-slug')
        else:
            return children
    def get_tags( self ):
        tags = []
        fotoalben = Fotoalbum.objects.live().descendant_of(self.get_site().root_page);
        for album in fotoalben:
            # Not tags.append() because we don't want a list of lists
            tags += album.get_tags()
        tags = sorted(set(tags))
        return tags

    def get_tagged_items( self, tag ):
        return Fotoalbum.objects.live().descendant_of(self.get_site().root_page).filter(tags__name=tag.name).order_by('-first_published_at');

    def get_context( self, request ):
        context = super(FotoalbumIndexPage, self).get_context( request )
        this_site = Site.find_for_request( request )

        tags = FotoalbumTag.objects.all()

        context['tags'] = tags

        return context        


    @route(r'^tags/$', name='tag_archive')
    @route(r'^tags/([-\w]+)/$', name='tag_archive')
    def tag_archive( self, request, tag = None):
        try:
            tag = Tag.objects.get(slug=tag)
        except Tag.DoesNotExist:
            return redirect(self.url)
        return TemplateResponse(
            request,
            'fotoalben/fotoalbum_index_tagged.html',
            {
                'tag' : tag, 
                'fotoalben': self.get_tagged_items(tag),
                'page' : self
            }
        )

    class Meta:
        verbose_name = 'Liste aller Fotoalben'



