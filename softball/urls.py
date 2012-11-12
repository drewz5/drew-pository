from django.conf.urls import patterns, include, url
from django.views.generic.simpole import direct_to_template

urlpatterns = patterns('softball.views',
                       url(r'^$', 'team_list', name='team_list'),
                       )
