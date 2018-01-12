from wagtail.wagtailcore import blocks
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtaildocs.blocks import DocumentChooserBlock
class ImageBlock( blocks.StructBlock ):
    img = ImageChooserBlock(
        required = True,
    )
    align = blocks.ChoiceBlock(
        choices = [
            ( 'LINKS', 'links' ),
            ( 'LINKS_SM', 'links, kleiner' ),
            ( 'RECHTS', 'rechts' ),
            ( 'RECHTS_SM', 'rechts, kleiner' ),
            ( 'FULL', 'ganze Breite'),
        ],
        label = 'Ausrichtung und Größe',
        required = True,
        help_text = 'Wie soll das Bild angezeigt werden?'
    )
    beschriftung = blocks.TextBlock(
        help_text = 'Dieser Text wird unterhalb des Bilds eingefügt',
        required = False
    )
    class Meta:
        icon = 'image'
        template = 'seiten/blocks/image.html'
        label = 'Bild'
        help_text = 'Ein einzelnes Bild im Textfluss'

class ImageAndCitationBlock( blocks.StructBlock ):
    img = ImageChooserBlock(
        required = True,
        label = 'Bild'
    )
    zitat = blocks.CharBlock(
        required = True,
        max_length = 256,
        label = 'Text'
    )

    class Meta:
        icon = 'image'
        template = 'scms2/blocks/image_and_citation.html'
        label = 'Bild und Text nebeneinander'
        help_text = 'Eine stark hervorgehobene Kombination aus Bild und kurzem Text.'
class Absatz( blocks.RichTextBlock ):
    def __init__(self, *args, **kwargs):
        kwargs['features'] = ['h4','h5','h6', 'bold','italic','ul','ol','link','document-link']
        super(Absatz, self).__init__(*args, **kwargs)
    class Meta:
        label = 'Text'
        help_text = 'Ein Textabsatz oder mehrere Textabsätze mit einfacher Formatierung und Links.'

class QuoteBlock( blocks.BlockQuoteBlock ):
    class Meta:
        label = 'Spruch'
        help_text = 'Ein kurzer Text, der hervorgehoben dargestellt wird.'

class YoutubeBlock( EmbedBlock ):
    class Meta:
        label = "Youtube-Video"
        help_text = 'Ein Youtube-Video, das in den Text eingefügt wird.'

class LocalVideoBlock( blocks.StructBlock ):
    standard = DocumentChooserBlock(
        label = 'Standard-Datei',
        help_text = 'Video-Datei für standarkonforme Browser (Container webm, Codec: V8.0, Audio: Ogg)'
    )
    alt1 = DocumentChooserBlock(
        label = 'Alternative 1',
        help_text = 'alternative Video-Datei (bspw. für Apple-Safari: Container mp4, Codec: H.264, Audio)',
        required = False
    )
    alt2 = DocumentChooserBlock(
        label = 'Alternative 2',
        help_text = 'alternative Video-Datei (bspw. für Internet-Explorer)',
        required = False
    )
    class Meta:
        label = 'Lokales Video'
        template = 'articles/blocks/video.html'
        help_text = 'Ein Video, das vom Schützen-Server geliefert wird und in den Text eingefügt wird.'

class VideoCarouselBlock( blocks.ListBlock ):
    def __init__(self, *args, **kwargs):
        super(VideoCarouselBlock, self).__init__(LocalVideoBlock(), *args, **kwargs)

    class Meta:
        label = "Video-Karussell"
        icon = "video"
        template = 'articles/blocks/video_karussell.html'
        help_text = 'Ein Video-Karussel mit Videos vom Schützen-Server.'

class ImageWithTextBlock( blocks.StructBlock ):
    image = ImageChooserBlock( required = True, label = 'Bild' )
    heading = blocks.TextBlock( required = False, label = "Titel" )
    subline = blocks.TextBlock( required = False, label = "Unterzeile" )
    subline2 = blocks.TextBlock( required = False, label = "Unterzeile 2" )
    size = blocks.ChoiceBlock(
        choices = [
            ( '150', 'klein (Breite: 150px)' ),
            ( '200', 'mittel (Breite: 200px)' ),
            ( '300', 'groß (Breite: 300px)'),
            ( '0', 'Bild nur verlinken, nicht anzeigen')
        ],
        label = 'Größe',
        required = True,
    )

    
    class Meta:
        template = 'scms2/blocks/image_with_text_block.html'
        
class ImgListBlock( blocks.ListBlock ):
    def __init__(self, *args, **kwargs):
        super(ImgListBlock, self).__init__(ImageWithTextBlock(), *args, **kwargs)

    class Meta:
        label = "BildListe"
        icon = "image"
        template = 'scms2/blocks/img_list_block.html'
        help_text = 'Eine Liste aus Bild und Text, nebeneinander, bspw. für Vorstands- oder Königslisten'

class OpenStreetMapBlock( blocks.CharBlock ):
    class Meta:
        label = 'Open-Streetmap-Karte'
        icon = "map"
        template = 'scms2/blocks/openstreetmap_map.html'
        help_text = 'Eine aus OpenStreetMap eingefügte Karte.'

class SitemapBlock(blocks.StaticBlock):
    class Meta:
        icon = 'user'
        label = 'Sitemap'
        admin_text = 'autmoatische Liste des Inhalts der Unterseiten'
        template = 'scms2/blocks/sitemap.html'
        help_text = 'Eine automatische Liste der Unterseiten.'
    
class HeadingBlock(blocks.CharBlock):
    class Meta:
        template = 'seiten/blocks/heading.html'
        help_text = 'Eine Überschrift.'
    
class Strophe(blocks.TextBlock):
    class Meta:
        template = 'scms2/blocks/strophe.html'
        icon = 'fa-music'
        help_text = 'Ein Text, dessen Umbrüche erhalten bleiben, bspw. für eine Liedstrophe.'

class Adresse(blocks.TextBlock):
    class Meta:
        template = 'scms2/blocks/adresse.html'
        icon = 'fa-address-card'
        help_text = 'Ein Text, dessen Umbrüche erhalten bleiben, für Adressen.'

class ComplexListItem(blocks.StructBlock):
    content = blocks.TextBlock(
        label = 'Inhalt'
    )
    level = blocks.ChoiceBlock(
        choices = (
            ('0','Ebene 1'),
            ('1','Ebene 2'),
            ('2','Ebene 3'),
            ('3','Ebene 4'),
        ),
        label = 'Ebene'
    )

class ComplexListBlock( blocks.ListBlock ):
    def __init__(self, *args, **kwargs):
        super(ComplexListBlock, self).__init__(ComplexListItem(), *args, **kwargs)
    class Meta:
        label = "komplexe Liste"
        icon = "fa-list-ol"
        template = 'scms2/blocks/complex_list_block.html'
        help_text = 'Eine Liste mit mehreren Ebenen, bspw. für Tagesordnungen.'
