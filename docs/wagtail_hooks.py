from django.conf.urls import url
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from wagtail.wagtailadmin.menu import MenuItem
from wagtail.wagtailcore import hooks

from . import views


@hooks.register('register_admin_urls')
def register_admin_urls():
    return [
        url(r'^doc/$', views.index, name='documentation'),
    ]


@hooks.register('register_admin_menu_item')
def register_help_menu_item():
    return MenuItem(
        'Hilfe',
        reverse('documentation'),
        classnames='icon icon-image',
        order=1000
    )
