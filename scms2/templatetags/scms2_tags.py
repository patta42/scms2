from articles.models import ArticlePage
from fotoalben.models import Fotoalbum

from django import template

from wagtail.wagtailcore.models import Site


register = template.Library()

@register.filter
def modulo(num, val):
    return num % val 

@register.filter
def natdiv(num, val):
    return int(num) // int(val)

@register.inclusion_tag('scms2/tags/shariff.html')
def shariff( page, id_ = None ):
    url = page.full_url
    if id_ is not None:
        url = url + '{}/'.format(id_)
    return{
        'url' : url
    }

@register.inclusion_tag(
    'scms2/tags/site_navigation.html', takes_context=True)
def site_navigation( context ):
    sites = Site.objects.all().order_by('site_name')
    current = Site.find_for_request( context['request'] )
    sites_info = [{
        'active' : site == current,
        'name' : site.root_page.title,
        'root' : site.root_page,
    } for site in sites ]
    return{
        'sites' : sorted(sites_info, key=lambda site: site['name']) 
    }
    
@register.inclusion_tag(
    'scms2/tags/footer.html', takes_context = True)
def footer( context ):
    current_site = context['request'].site
    n_sites = len( Site.objects.all() )
    articles = ArticlePage.objects.live().order_by('-date')
    latest_articles = {};
    for article in articles:
        site = article.get_site()
        if site != current_site and site not in latest_articles:
            latest_articles[site] = article
            if len( latest_articles ) == n_sites - 1:
                break
    l_articles = [{
        'page' : page,
        'site' : site,
        'date' : page.get_article_date()
    } for site, page in latest_articles.items() ]
    return {
        'latest_articles' : l_articles
    }

@register.simple_tag( takes_context = True )
def current_site( context ):
    return context['request'].site.site_name
    

@register.simple_tag()
def call_render_as_child( page, depth = -1 ):
    return page.render_as_child( depth )

@register.inclusion_tag( 'scms2/tags/footer_alben.html' )
def footer_alben ( page ):
    site = page.get_site()
    alben = []
    for website in Site.objects.exclude(id=site.id).all():
        alben.append(
            {
                'name': website.site_name, 
                'album' : Fotoalbum.objects.in_site(website).order_by('-first_published_at').first()
            }
        )
    return { 'alben' : alben }

@register.inclusion_tag( 'scms2/tags/footer_article.html' )
def footer_article ( page ):
    site = page.get_site()
    articles = []
    for website in Site.objects.exclude(id=site.id).all():
        articles.append(
            {
                'name': website.site_name, 
                'article' : ArticlePage.objects.in_site(website).order_by('-date').first()
            }
        )
    return { 'articles' : articles }

