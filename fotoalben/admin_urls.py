from django.conf.urls import url

from .views import multichooser,multichooser_select

urlpatterns = [
    url(r'^multichooser/select/$', multichooser_select, name='chooser-select'),   
    url(r'^multichooser/$', multichooser, name='chooser'),

]
