from .models import Fotoalbum

from wagtail.wagtailcore import blocks
from wagtail.wagtailimages.blocks import ImageChooserBlock


class FotoalbumBlock( blocks.StructBlock ):
    album = blocks.PageChooserBlock(
        required = True,
        target_model = Fotoalbum,
        label = 'Fotoalbum auswählen'
    )
    show_as = blocks.ChoiceBlock(
        choices = [
            ('single', 'Einzelnes Bild'),
            ('carousel', 'Bilderkarussell'),
        ],
        help_text = 'Wie soll das Fotoalbum angezeigt werden?',
        label = 'Anzeige als',
        default = 'single'
    )
    auto_caption = blocks.BooleanBlock(
        required = False,
        label = "Automatische Bildunterschrift",
        help_text = 'Soll die Bildunterschrift automatisch aus den Informationen für das Bild generiert werden?'
    )
    caption = blocks.CharBlock(
        required = False,
        max_length = 256,
        label = 'Manuelle Bildunterschrift',
    )
   
    style = blocks.ChoiceBlock(
        choices = [
            ('full','Volle Breite'),
            ('left_sm', 'klein, links im Text'),
            ('left_med', 'mittelgroß, links im Text'),
            ('right_sm', 'klein, rechts im Text'),
            ('right_med', 'mittelgroß, rechts im Text'),
        ],
        help_text = 'Bei Anzeige als Einzelbild: Wo soll das Bild platziert werden?',
        verbose_name = 'Anzeigeoptionen',
        required = False,
        default = 'full'
    )
    link = blocks.BooleanBlock(
        required = False,
        default = True,
        verbose_name = 'Link',
        help_text = 'Link zum Album einfügen?'
    )

    class Meta:
        icon = 'image'
        template = 'fotoalben/blocks/fotoalbum_block.html'
        label = 'Fotoalbum'
