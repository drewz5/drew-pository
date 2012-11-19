from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    url(r'^$', 'softball.views.team_list', name='team_list'),
    url(r'^team/(?P<team_id>\d+)/$', 'softball.views.team_view', name='team_view'),
)

