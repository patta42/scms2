from ..models import get_next
from django import template


register = template.Library()

@register.inclusion_tag( 'termine/tags/next_event.html', takes_context = True )
def next_event( context ):
    return { 
        'next': get_next( context ),
    }
