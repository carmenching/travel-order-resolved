from sncf_final.views import *
from django.urls import path
from sncf_final.templates import templates

urlpatterns = [
    path('bestPathAudio',anyToAny),
    path('bestPath',test),
    path('names',getAllStations),
    path('', templates.index, name='index')

]