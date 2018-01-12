from wagtail.contrib.settings.models import BaseSetting, register_setting
from django.db import models

@register_setting
class SocialMediaSettings(BaseSetting):
    facebook = models.URLField(
        help_text='Your Facebook page URL',
        null = True,
        blank = True,
    )
    youtube = models.URLField(
        help_text='Your YouTube channel or user account URL',
        null = True,
        blank = True,
    )
    
class Kontaktperson(BaseSetting):
    class Meta:
        abstract = True

    position = models.CharField(
        max_length = 128,
        verbose_name = 'Position',
        help_text = 'bspw. Oberst, Kompanieführer'
    )
    name = models.CharField(
        max_length = 128,
        verbose_name = 'Vorname Name'
    )
    strasse = models.CharField(
        max_length = 128
    )
    plzort = models.CharField(
        max_length = 128,
        verbose_name = 'PLZ Ort'
    )
    tel = models.CharField(
        max_length = 128,
        verbose_name = 'Telefon'
    )
    email = models.CharField(
        max_length = 128,
        verbose_name = 'E-Mail',
        blank = True
    )

@register_setting
class Hauptkontaktperson(Kontaktperson):
    pass
@register_setting
class Zweitkontaktperson(Kontaktperson):
    pass

@register_setting
class VISDP(Kontaktperson):
    position = None
    class Meta:
        verbose_name = 'Verantwortlich für den Inhalt'

