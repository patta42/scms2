from wagtail.wagtailcore import hooks
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.utils.html import format_html, format_html_join
from django.core import urlresolvers
from django.conf.urls import url, include
from . import admin_urls

@hooks.register('register_admin_urls')
def register_admin_urls():
    return [
        url(r'^fotoalben/', include(admin_urls, namespace='fotoalben', app_name='fotoalben')),
]

@hooks.register('insert_editor_js')
def editor_js():
    js_files = [
        static('fotoalben/js/inline-image-panel.js'),
    ]
    js_includes = format_html_join(
        '\n', '<script src="{0}"></script>',
        ((filename, ) for filename in js_files)
    )
    return js_includes + format_html(
        """
        <script>
               window.chooserUrls.inlineImageChooser = '{0}';
        </script>
        """, urlresolvers.reverse('fotoalben:chooser'))
