# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       # statics are served outside

                       (r'^$',
                        'django.views.generic.simple.redirect_to',
                        {'url': 'main/', 
                         # can we make this a call, instead of a string?
                         'query_string': True,
                         'permanent': False, 
                         # SET THIS TO TRUE IN PRODUCTION!
                         }),

                       # the media files SHOULD be served as the statics
                       (r'media/(.*)',
                        'django.views.static.serve',
                        {'document_root': settings.MEDIA_ROOT}),

                       # admin
                       #url(r'^admin/', include(admin.site.urls)),
                       
                       # log in/out
                       # url(r'login/$',
                       #     'django.contrib.auth.views.login',
                       #     name='login'),
                       # url(r'logout/$',
                       #     'django.contrib.auth.views.logout',
                       #     name='logout'),

                       (r'^main/', include('main.urls',
                                           namespace='main')),
                       )
