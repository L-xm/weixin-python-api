# -*- coding: utf8 -*-
from weixin import Conf
conf = Conf()

def trans_userinfo(data):
    transkey = conf.get('transkey')
    new_data = []
    for old_key, new_key in transkey:
        value = data.get(old_key, '')
        if old_key == 'sex':
            transsex = conf.get('transsex')
            value = transsex.get(value)
        if old_key == 'privilege':
            value = ','.join(value)
        new_data.append((new_key, value))
    return new_data
