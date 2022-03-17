# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'website',
        'USER': 'root',
        'PASSWORD': 'xianjian1998',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

#腾讯云短信应用app_id
TENCENT_SMS_APP_ID = 1400632003
#腾讯云短信的app_key
TENCENT_SMS_APP_KEY = "178c45c93e06ca4ce2bbf70b7b617a8e"
#腾讯云短信签名内容
TENCENT_SMS_SIGN = "林音三弦个人公众号"

#腾讯cos的id和key
COS_SECRET_ID = 'AKIDaz81e05tPecJkvpTqwqTqypQknZ4IH1U'   # 替换为用户的 secretId
COS_SECRET_KEY = 'DApDKAk36sNaMrHTP5UcU6RVIq77rQkn'

CACHES = {
    "default": {
        'BACKEND': 'django_redis.cache.RedisCache',
        "LOCATION": "redis://127.0.0.1:6379/1",
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'CONNECTION_POLL_KWARGS': {
                'max_connections': 1000,
                'encoding': 'utf-8'
            },
            'PASSWORD': 'xianjian1998'
}
    }
}