# -*- coding: utf8 -*-
# weixin api configure file

######### app configure ###############
token = 'sLg2Xr3teB5KlXOd'
appid = '*************' # 填写你的appid
appsecret = '********************'  #填写你的appsecret

######### api url configure ###############
# 获取access_token
token_api_url = 'https://api.weixin.qq.com/cgi-bin/token'
# 获取微信服务器ip列表
backip_api_url = 'https://api.weixin.qq.com/cgi-bin/getcallbackip'
# 获取关注用户列表
userlist_api_url = 'https://api.weixin.qq.com/cgi-bin/user/get'
# OAuth2.0验证,通过网页授权得到的code获取access_code
oauth2_api_url = 'https://api.weixin.qq.com/sns/oauth2/access_token'
# OAuth2.0验证，刷新access_token
oauth2_refreshtoken_api_url = 'https://api.weixin.qq.com/sns/oauth2/refresh_token'
# OAuth2.0验证，获取用户信息
oauth2_userinfo_api_url = 'https://api.weixin.qq.com/sns/userinfo'
# 检查access_token是否有效
check_auth_api_url = 'https://api.weixin.qq.com/sns/auth'

######### 用户信息中英转换 ###############
transkey = [('openid', 'openid'),
            ('nickname', '昵称'),
            ('sex', '性别'),
            ('headimgurl', '头像'),
            ('province', '省份'),
            ('city', '城市'),
            ('country', '国家'),
            ('language', '语言'),
            ('privilege', '特权信息'),
            ('unionid', 'unionid')]

######### 性别转换 ######################
transsex = {1: '男', 2: '女', 0: '未知'}