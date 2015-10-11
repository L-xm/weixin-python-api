# -*- coding: utf8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns('wechat.views',
    url(r'^$', 'home', name='home'),
    url(r'^check/$', 'check_signature', name='check_signature'),
    url(r'^userinfo/$', 'display_userinfo', name='userinfo'),
    # url(r'^test_userinfo/$', 'test_userinfo')
    )