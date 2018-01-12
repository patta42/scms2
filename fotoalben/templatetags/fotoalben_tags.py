from django import template

register = template.Library()

@register.inclusion_tag('fotoalben/tags/css_selectors.css')
def css_selectors( max_num ):
    return {
        'sections' : range(max_num)
    }

@register.inclusion_tag('fotoalben/tags/subpage_nav.html')
def subpage_nav( current, max_ ):
    return {
        'curr' : current,
        'max' : max_
    }
@register.inclusion_tag('fotoalben/tags/baguette_box.html')
def baguette_box_html( images ):
    return {
        'images' : images
    }

