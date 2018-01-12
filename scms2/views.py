from django.shortcuts import render
from wagtail.wagtailcore.models import Site

from .models import Hauptkontaktperson, VISDP

def kontakt( request ):
    return render(request, 'scms2/kontakt.html',{
        'site' : request.site,
        'page' : request.site.root_page,
    });

def impressum( request ):
    contacts = []
    responsibles = []

    for site in Site.objects.all():
        contacts.append({'site': site, 'person': Hauptkontaktperson.for_site(site) })
        responsibles.append({'site': site, 'person': VISDP.for_site(site) })


    return render(request, 'scms2/impressum.html',{
        'contacts' : contacts,
        'responsibles': responsibles,
        'page' : request.site.root_page,
    });
    
