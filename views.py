# -*- coding: utf8 -*-

from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse, Http404
from django.core.urlresolvers import reverse
from weixin import WeiXinBasic, WeiXinUserManager, Conf
import utils
import urllib

conf = Conf()
# wx_basic = WeiXinBasic()
# wx_usermanager = WeiXinUserManager()

def home(request):
    if request.session.has_key('oauth_data'):
        data = request.session['oauth_data']
        access_token = data['access_token']
        openid = data['openid']
        wx_usermanager = WeiXinUserManager()
        if not wx_usermanager.check_auth(access_token, openid):
            data = wx_usermanager.refresh_oauth2_access_token(
                                    data['refresh_token'])
            request.session['oauth_data'] = data
            access_token = data['access_token']
            openid = data['openid']
        data = wx_usermanager.get_userinfo(access_token, openid)
        data = utils.trans_userinfo(data)
        return render_to_response('wechat/display_userinfo.html',
                                  {'userinfo': data})
    redirect_uri = urllib.quote_plus('http://slience.xyz' + reverse('wechat:userinfo'))
    context = {'appid': conf.get('appid'),
               'redirect_uri': redirect_uri,
               'scope': 'snsapi_userinfo',
               'state': 'userinfo'}
    return render_to_response('wechat/index.html', context)

def display_userinfo(request):
    if request.session.has_key('oauth_data'):
        data = request.session['oauth_data']
        access_token = data['access_token']
        openid = data['openid']
        wx_usermanager = WeiXinUserManager()
        if not wx_usermanager.check_auth(access_token, openid):
            data = wx_usermanager.refresh_oauth2_access_token(
                                    data['refresh_token'])
            request.session['oauth_data'] = data
            access_token = data['access_token']
            openid = data['openid']
        data = wx_usermanager.get_userinfo(access_token, openid)
        data = utils.trans_userinfo(data)
        return render_to_response('wechat/display_userinfo.html',
                                  {'userinfo': data})
    code = request.GET.get('code')
    state = request.GET.get('state')
    if code is None:
        # 授权失败
        return render_to_response('wechat/error.html')
    wx_usermanager = WeiXinUserManager()
    data = wx_usermanager.get_oauth2_access_token(code)
    request.session['oauth_data'] = data
    return redirect(reverse('wechat:userinfo'))

# def test_userinfo(request):
#     data = [('openid', '254q433te'), ('昵称', 'lxy'), ('性别', '男'),
#             ('头像', 'http://i12.tietuku.com/bd8343a279581d44.jpg'),
#             ('省份', '广西'), ('城市', '桂林'), ('国家','中国'),
#             ('语言', '汉语'), ('特权信息', [])]
#     return render_to_response('wechat/display_userinfo.html',
#                                   {'userinfo': data})
def check_signature(request):
    signature = request.GET.get('signature')
    timestamp = request.GET.get('timestamp')
    nonce = request.GET.get('nonce')
    echostr = request.GET.get('echostr')
    wx_basic = WeiXinBasic()
    if wx_basic.check_signature(signature, timestamp, nonce):
        return HttpResponse(echostr)
    raise Http404('check signature failed')
