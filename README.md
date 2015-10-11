## 微信公众平台 python接口(不完全，只包含基础接口和网页授权认证接口)

### 这是一个独立的django app.按照下面的步骤安装到你的项目中

1. 在URLConf中添加下面的url配置就可以了
```python
from django.conf.urls import patterns, include, url
import views
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('',
        #...
        url(r'^wechat/', include('wechat.urls'), namespace='wechat'), # 新增url
)
```

2. 在settings.pyz中添加app
```
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    #...
    'wechat', # 新增app
)
```
3. 在微信客户端打开`http://yoursite/wechat/`,显示网页授权链接:
`https://open.weixin.qq.com/connect/oauth2/authorize?appid=APPID&redirect_uri=REDIRECT_URI&response_type=code&scope=SCOPE&state=STATE#wechat_redirect`
**redirect_uri一定要使用urlencode进行编码,python中可使用`urllib.urlencode`**
4. 点击该链接,显示用户基本信息
5. 服务器会在session中保存access_token, openid, refresh_token. 下次访问个人信息时,不会出现授权页,而是直接显示用户信息.

### api使用方法
- 首先需要在weixin/conf.py中配置开发者的token, appid, appsecret.
conf.py包含api的url信息以及其它相关信息.

- Example
```python
In [1]: from weixin import WeiXinBasic, WeiXinUserManager, Conf

# 检查signature.当在微信公众平台--开发者中心配置服务器接口信息时需要用到.
# signature正确无误,返回True, 否则返回False.
wx_basic.check_signature(signature, timestamp, nonce)

# 基础api
In [2]: wx_basic = WeiXinBasic()
# 获取access_token
In [3]: json_data = wx_basic.get_access_token()

In [4]: json_data
Out[4]:
{u'access_token': u'ZM2nEmxwH_7cHWtVBa9YlPgX96-1Hvcg1gJkfYQz0mDvbVrF9Ecq1qcydRBKn-4n-JWfOSAGXh3OUCDrPukTGzdtOm8dYyLW9x2Dq3xUTdI',
u'expires_in': 7200}
# 获取微信服务器ip列表
In [5]: wx_basic.get_backip(json_data['access_token'])
Out[5]:
{u'ip_list': [u'101.226.62.77',
  u'101.226.62.78',
  u'101.226.62.79',
  u'101.226.62.80',
  u'101.226.62.81',
  u'101.226.62.82',
  u'101.226.62.83',
  u'101.226.62.84',
  u'101.226.62.85',
  ]}
# 省略了一部分ip

# 用户管理api
In [6]: wx_usermanager = WeiXinUserManager()
# 获取关注公众号的用户列表
In [7]: wx_usermanager.get_user_list(json_data['access_token'])
Out[7]:
{u'count': 1,
 u'data': {u'openid': [u'oIe2qt8Z-kfzuWTyGwGk93ntnIYo']},
 u'next_openid': u'oIe2qt8Z-kfzuWTyGwGk93ntnIYo',
 u'total': 1}

# 其它method在命令行不方便演示,只给出使用方法
# code由微信服务器通过redirect_uri/?code=CODE?state=STATE传递给你自己的网站
wx_usermanager.get_oauth2_access_token(code)
# 刷新access_token
wx_usermanager.refresh_oauth2_access_token(refresh_token)
# 获取用户信息
wx_usermanager.get_userinfo(access_token, openid, lang='zh_CN')
# 检查access_token是否有效,有效返回True,否则返回False
wx_usermanager.check_auth(self, access_token, openid)

# api Conf
In [9]: conf = Conf()

In [10]: conf.get('token')
Out[10]: 'naegrigedr'

In [11]: conf.get('appid')
Out[11]: 'eraheatajsrtjst6yjir'

In [12]: conf.get('appsecret')
Out[12]: 'sdrhserhoershjoihrsohji'

In [13]: conf.get('token_api_url')
Out[13]: 'https://api.weixin.qq.com/cgi-bin/token'

In [14]: conf.get('oauth2_api_url')
Out[14]: 'https://api.weixin.qq.com/sns/oauth2/access_token'
```

