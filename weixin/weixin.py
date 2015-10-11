# -*- coding: utf8 -*-

import requests

class ErrorMsg(Exception):
    ''' exception for error code returned by api
    '''
    def __init__(self, errmsg):
        self.errmsg = errmsg

    def __str__(self):
        return str(self.errmsg)

class Conf(object):
    '''读取配置文件
    '''
    def __init__(self):
        import conf
        self._conf = dict(filter(lambda item: not item[0].startswith('__'),
                                 conf.__dict__.iteritems()))

    def get(self, key, default=None):
        return self._conf.get(key, default)

conf = Conf()

def api_request(method, api_url, params):
    import json
    if method == 'get':
        res = requests.get(api_url, params=params)
    elif method == 'psot':
        headers = {'content-type': 'application/json;encoding=utf8'}
        res = requests.post(api_url, headers=headers, data=json.dumps(params))
    if res.status_code != 200:
        res.raise_for_status()  
    return json.loads(res.content)

class WeiXinBasic(object):
    '''基础api支持
    '''
    def __init__(self):
        self.token = conf.get('token')

    def check_signature(self, signature, timestamp, nonce):
        '''检查signature
        '''
        import hashlib
        str_list = [self.token, timestamp, nonce]
        str_list.sotr()
        combind_str = ''.join(str_list)
        encrypt_str = hashlib.sha1(combind_str).hexdigest()
        if encrypt_str == signature:
            return True
        return False

    def get_access_token(self):
        '''获取access_token
        '''
        params = {'grant_type': 'client_credential', 
                  'appid': conf.get('appid'),
                  'secret': conf.get('appsecret')}
        return_json = api_request('get', conf.get('token_api_url'), params)
        if return_json.has_key('access_token'):
            return return_json
        raise ErrorMsg(return_json)

    def get_backip(self, access_token):
        params = {'access_token': access_token}
        return_json = api_request('get', conf.get('backip_api_url'), params)
        if return_json.has_key('ip_list'):
            return return_json
        raise ErrorMsg(return_json)

    def update_token(self, access_token):
        pass

class WeiXinUserManager(object):
    '''用户管理api
    '''
    def __init__(self):
        pass

    def get_user_list(self, access_token, next_openid=''):
        params = {'access_token': access_token,
                  'next_openid': next_openid}
        return_json = api_request('get', conf.get('userlist_api_url'),
                                  params)
        if return_json.has_key('total'):
            return return_json
        # raise ErrorMsg
        raise ErrorMsg(return_json)
    
    def get_oauth2_access_token(self, code):
        params = {'appid': conf.get('appid'),
                  'secret': conf.get('appsecret'),
                  'code': code,
                  'grant_type': 'authorization_code'}
        return_json = api_request('get', conf.get('oauth2_api_url'), params)
        if return_json.has_key('access_token'):
            return return_json
        raise ErrorMsg(return_json)

    def refresh_oauth2_access_token(self, refresh_token):
        params = {'appid': conf.get('appid'),
                  'grant_type': 'refresh_token',
                  'refresh_token': refresh_token}
        return_json = api_request('get',
                                  conf.get('oauth2_refreshtoken_api_url'),
                                  params)
        if return_json.has_key('access_token'):
            return return_json
        raise ErrorMsg(return_json)

    def get_userinfo(self, access_token, openid, lang='zh_CN'):
        '''@param:lang    value of lang is the one of following:zh_CN,zh_TW,en
        '''
        params = {'access_token': access_token,
                  'openid': openid,
                  'lang': lang}
        return_json = api_request('get',
                                  conf.get('oauth2_userinfo_api_url'),
                                  params)
        if return_json.has_key('openid'):
            return return_json
        raise ErrorMsg(return_json)

    def check_auth(self, access_token, openid):
        params = {'access_token': access_token, 'openid': openid}
        return_json = api_request('get', conf.get('check_auth_api_url'),
                                  params)
        if return_json['errcode'] == 0 and return_json['errmsg'] == 'ok':
            return True
        return False

if __name__ == '__main__':
    wx_basic = WeiXinBasic()
    json_data = wx_basic.get_access_token()
    access_token = json_data['access_token']
    print wx_basic.get_backip(access_token)['ip_list']
    
