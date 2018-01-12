from wagtail.wagtailcore import blocks

class TOCBlock(blocks.StaticBlock):
    class Meta:
        label = 'Inhaltsverzeichnis'
        icon = 'fa-list-ol'
        admin_text = 'automatisch generierte Liste der Überschriften auf dieser Seite'
