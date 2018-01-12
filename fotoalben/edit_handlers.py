import django
from wagtail.wagtailimages.edit_handlers import BaseImageChooserPanel
from wagtail.wagtailadmin.edit_handlers import InlinePanel, \
    BaseInlinePanel, widget_with_script
from .widgets import AdminMultiImageChooser
from django.template.loader import render_to_string
from wagtail.wagtailimages.fields import ALLOWED_EXTENSIONS


class BaseInlineImagePanel( BaseInlinePanel ):
    js_template = 'fotoalben/js/inline-image-panel.tpl.js'    
    template = 'fotoalben/html/inline_image_panel.html'

    def render(self):
        formset = render_to_string(self.template, {
            'self': self,
            'can_order': self.formset.can_order,
            'allowed_extensions': ALLOWED_EXTENSIONS,
            'max_filesize':10*1024*1024,
            'error_max_file_size': 'File too large',
            'error_accepted_file_types': 'Filetype not allowed',
            'help_text': 'add your files here',
        })
        js = self.render_js_init()
        return widget_with_script(formset, js)


class InlineImagePanel( object ):
    def __init__(self, relation_name, panels=None, classname='', label='', help_text='', min_num=None, max_num=None):
        self.relation_name = relation_name
        self.panels = panels
        self.label = label
        self.help_text = help_text
        self.min_num = min_num
        self.max_num = max_num
        self.classname = classname

    

    def bind_to_model( self, model ):
        if django.VERSION >= (1, 9):
            related = getattr(model, self.relation_name).rel
        else:
            related = getattr(model, self.relation_name).related

        return type(str('_ImageInlinePanel'), (BaseInlineImagePanel,), {
            'model': model,
            'relation_name': self.relation_name,
            'related': related,
            'panels': self.panels,
            'heading': self.label,
            'help_text': self.help_text,
            # TODO: can we pick this out of the foreign key definition as an alternative?
            # (with a bit of help from the inlineformset object, as we do for label/heading)
            'min_num': self.min_num,
            'max_num': self.max_num,
            'classname': self.classname,
        })
