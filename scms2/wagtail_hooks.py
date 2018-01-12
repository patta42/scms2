from django.contrib.staticfiles.templatetags.staticfiles import static
from django.utils.html import format_html

from wagtail.wagtailcore import hooks
@hooks.register('insert_editor_css')
def editor_css():
    return format_html(
        '''<link rel="stylesheet" href="{}">
        <link rel="stylesheet" href="{}">''',
        static('css/admin/customizable-richtext.css'),
        static('css/admin/font-awesome.min.css'),
    )
@hooks.register('insert_global_admin_css')
def global_admin_css():
    return format_html(
        '<link rel="stylesheet" href="{}"></link>',
        static('css/admin/collection-chooser.css'),
    )

@hooks.register('insert_global_admin_js')
def global_admin_js():
    return format_html(
        '<script src="{}"></script>',
        static('js/admin/collection-chooser.js'),
    )
    
