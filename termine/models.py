import datetime
 
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import models
from django.forms import widgets

from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailcore.models import Page, Orderable, Site


# Create your models here.


class TerminListe( Page ):
    icon = "calendar"
    subpage_types = [ 'termine.Termin' ]
    is_creatable = False
    einleitung = models.TextField(
        blank = True,
        null = True,
        max_length = 1024,
        help_text = 'Kurze Einleitung, die zu Beginn der Auflistungsseite erscheint.' 
    )
    vergangene_termine = models.BooleanField(
        help_text = ( 'Sollen vergangene Termine angezeigt werden?' ),
        default = False,
        verbose_name =  'Vergangene Termine anzeigen?'
    )

    content_panels = Page.content_panels + [
        FieldPanel('einleitung'),
        FieldPanel('vergangene_termine'),
    ]
    def get_icon(self):
        return self.icon

    def get_context( self, request ):
        this_site = Site.find_for_request( request )
        context = super(TerminListe, self).get_context( request )
        alle_termine = Termin.objects.live().filter( datum__gte = datetime.datetime.now() ).order_by( 'datum' )
        termine = [ termin for termin in alle_termine if termin.get_site() == this_site ]
        paginator = Paginator( termine, 30 )
        page = request.GET.get( 'page' )
        try:
            termine = paginator.page( page )
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            termine = paginator.page( 1 )
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            termine = paginator.page( paginator.num_pages )
        context['termine'] = termine

        return context

    class Meta:
        verbose_name = 'Liste der Termine'
    
def get_next( context ):
    """
    This is called from the template tag 'next_event'
    returns the next event for a site
    """
    return Termin.objects.live().descendant_of(context['request'].site.root_page).filter( datum__gte = datetime.datetime.now() ).order_by('datum').first()
    # termin = None
    # for termin in alle_termine:
    #     if termin.get_site() == context['request'].site:
    #         break
    # return termin


class Termin ( Page ):
    parent_page_types = [ 'termine.TerminListe' ]
    subpage_types = []
    datum = models.DateField()
    enddatum = models.DateField(
        null = True,
        blank = True
    )
    uhrzeit = models.TimeField(
        blank = True,
        null = True
    )
    beschreibung = models.TextField(
        blank = True,
        null = True,
        
    )

    content_panels = Page.content_panels + [
        FieldPanel('datum'),
        FieldPanel('uhrzeit'),
        FieldPanel('enddatum'),
        FieldPanel('beschreibung', widget = widgets.Textarea()),
    ]

    def get_next( request ):
        this_site = Site.find_for_request( request )
        alle_termine = Termin.objects.live().filter( datum__gte = datetime.datetime.now()).order_by('datum')
        termine = [ termin for termin in alle_termine if termin.get_site() == this_site ]
        try:
            return termine[0]
        except IndexError:
            return []

    def __str__( self ):
        return "{} - {}".format( self.title, self.datum )
