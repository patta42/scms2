from wagtail.wagtailimages.widgets import AdminImageChooser
from django.utils.translation import ugettext_lazy as _
import json

class AdminMultiImageChooser( AdminImageChooser ):
    choose_one_text = _('Choose images')

    def render_js_init(self, id_, name, value):
        return "createImageChooser({0});".format(json.dumps(id_))
