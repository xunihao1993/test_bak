"""
Django settings for {{ project_name }} project.

Generated by 'django-admin startproject' using Django {{ django_version }}.

For more information on this file, see
https://docs.djangoproject.com/en/{{ docs_version }}/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/{{ docs_version }}/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/{{ docs_version }}/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '{{ secret_key }}'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*', ]

# Application definition

INSTALLED_APPS = [
	'simpleui',
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
]

MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [],
		'APP_DIRS': True,
		'OPTIONS': {
			'context_processors': [
				'django.template.context_processors.debug',
				'django.template.context_processors.request',
				'django.contrib.auth.context_processors.auth',
				'django.contrib.messages.context_processors.messages',
			],
		},
	},
]

WSGI_APPLICATION = 'project.wsgi.application'

# Database
# https://docs.djangoproject.com/en/{{ docs_version }}/ref/settings/#databases

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.mysql',
		'NAME': 'filedown',
		'USER': 'root',
		'PASSWORD': 'root',
		'HOST': 'localhost',
		'POST': '3306',
	}
}

# 配置缓存
CACHES = {
	'default': {
		'BACKEND': 'redis_cache.cache.RedisCache',
		'LOCATION': "redis://127.0.0.1:6379/0",
		'TIMEOUT': 60,
		"OPTIONS": {
			"CLIENT_CLASS": "django_redis.client.DefaultClient",
		}
	}
}

# Password validation
# https://docs.djangoproject.com/en/{{ docs_version }}/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
	{
		'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
	},
]

# Internationalization
# https://docs.djangoproject.com/en/{{ docs_version }}/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/{{ docs_version }}/howto/static-files/

STATIC_URL = '/static/'

ENV = 'local'
SERVER_ADDRESS = 'xxx.xxx.xxx.xxx'

# Carrier地址
AUTH_SERVER_ENDPOINT = 'http://xxx.xxx.xxx.xxx:8080'
# 本项目的 CLIENT_ID 和 CLIENT_SECRET
AUTH_SERVER_CLIENT_ID = '*******************'
AUTH_SERVER_CLIENT_SECRET = '******************************************'

MANAGER = [
	'lizhiwei11',
	'sumuzhong'
]

INSTALLED_APPS = INSTALLED_APPS + [
	'rest_framework',
	'commissionApp',
	'djcelery',
]

if ENV != 'prod':
	INSTALLED_APPS = INSTALLED_APPS + ['corsheaders']
	MIDDLEWARE.insert(MIDDLEWARE.index('django.contrib.sessions.middleware.SessionMiddleware'),
					  'corsheaders.middleware.CorsMiddleware')
	# 跨域增加忽略
	CORS_ALLOW_CREDENTIALS = True
	CORS_ORIGIN_ALLOW_ALL = True
	CORS_ORIGIN_WHITELIST = ('*',)

	CORS_ALLOW_METHODS = (
		'DELETE',
		'GET',
		'OPTIONS',
		'PATCH',
		'POST',
		'PUT',
		'VIEW',
	)

	CORS_ALLOW_HEADERS = (
		'XMLHttpRequest',
		'X_FILENAME',
		'accept-encoding',
		'authorization',
		'content-type',
		'dnt',
		'origin',
		'user-agent',
		'x-csrftoken',
		'x-requested-with',
		'Pragma',
	)

# MIDDLEWARE = MIDDLEWARE + ['{{ project_name }}.middleware.InterfaceVisitedTrackMiddleware']

REST_FRAMEWORK = {
	'DEFAULT_PERMISSION_CLASSES': [
		'rest_framework.permissions.IsAuthenticated',
	],
	'DEFAULT_AUTHENTICATION_CLASSES': [
		'commissionApp.authentication.ExpiringTokenAuthentication',
		'rest_framework.authentication.SessionAuthentication',
	],
	'EXCEPTION_HANDLER': 'commissionApp.utils.exceptions.exception_handler'
}

# logging 配置
# 日志处理
BASE_LOG_DIR = os.path.join(BASE_DIR, "logs")
if not os.path.exists(BASE_LOG_DIR):
	os.makedirs(BASE_LOG_DIR)
LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,
	# 日志输出格式的定义
	'formatters': {
		'verbose': {
			'format': '%(levelname)s [%(asctime)s] [%(pathname)s %(funcName)s %(lineno)s] %(message)s'
		},
	},
	# 处理器：需要处理什么级别的日志及如何处理
	'handlers': {
		# 将日志打印到终端
		'console': {
			'level': 'INFO',  # 日志级别
			'class': 'logging.StreamHandler',  # 使用什么类去处理日志流
			'formatter': 'verbose'  # 指定上面定义过的一种日志输出格式
		},
		# 默认日志处理器
		'default': {
			'level': 'INFO',
			'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
			'filename': os.path.join(BASE_LOG_DIR, "commissionApp.log"),  # 日志文件路径
			'maxBytes': 1024 * 1024 * 10,  # 日志大小 10M
			'backupCount': 5,  # 日志文件备份的数量
			'formatter': 'verbose',  # 日志输出格式
			'encoding': 'utf-8',
		},
		# 日志处理级别warn
		'warn': {
			'level': 'WARN',
			'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
			'filename': os.path.join(BASE_LOG_DIR, "warn.log"),  # 日志文件路径
			'maxBytes': 1024 * 1024 * 100,  # 日志大小 100M
			'backupCount': 5,  # 日志文件备份的数量
			'formatter': 'verbose',  # 日志格式
			'encoding': 'utf-8',
		},
		# 日志级别error
		'error': {
			'level': 'ERROR',
			'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
			'filename': os.path.join(BASE_LOG_DIR, "error.log"),  # 日志文件路径
			'maxBytes': 1024 * 1024 * 100,  # 日志大小 100M
			'backupCount': 5,
			'formatter': 'verbose',  # 日志格式
			'encoding': 'utf-8',
		},
	},

	'loggers': {
		# 默认的logger应用如下配置
		'': {
			'handlers': ['default', 'warn', 'error', 'console'],
			'level': 'INFO',
			'propagate': True,  # 如果有父级的logger示例，表示不要向上传递日志流
		},
	},
}
'''
celery
'''
# 配置celery
import djcelery

djcelery.setup_loader()
# 指定redis数据库
# CELERY_BROKER_URL = 'redis://:haohao@192.168.45.90:6379/0'
BROKER_URL = 'redis://127.0.0.1:6379/1'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/1'
# CELERY_RESULT_BACKEND = 'django-db'
CELERY_RESULT_SERIALIZER = 'json'


CELERYD_CONCURRENCY = 2      # celery worker并发数
CELERYD_MAX_TASKS_PER_CHILD = 5   # 每个worker最大执行任务数


# celery时区设置，使用settings中TIME_ZONE同样的时区
CELERY_TIMEZONE = TIME_ZONE
# 指定任务文件
CELERY_IMPORES = ("commissionApp.task")  # app.task**********
# celery beat配置
DJANGO_CELERY_BEAT_TZ_AWARE = False
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
# from celery.schedules import crontab
# CELERYBEAT_SCHEDULE = {
# 	u'测试11111': {
# 		"task": "commissionApp.task.longIO",  # ******** app.task
# 		"schedule": crontab(),
# 		"args": (['1', '2'], ['3', '4'])  # 传参，可以以文件的形式动态读取
# 	},
# }

APP_ERROR_CODE_ID = '999'
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
# STATIC_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
exec('from commissionApp.properties.{} import *'.format(ENV))

'''
simpleui

'''
import time
from commissionApp.toolkit.general_tools import get_ip

flowerUrl = 'http://%s:9008/' % get_ip()
# SIMPLEUI_ICON = {
# 	'系统管理': 'fab fa-apple',
# 	'员工管理': 'fas fa-user-tie'
# }
SIMPLEUI_HOME_INFO = False
SIMPLEUI_CONFIG = {
	'system_keep': False,
	# 'menu_display': ['综合信息管理', '定时异步任务管理', '权限认证', ],  # 开启排序和过滤功能, 不填此字段为默认排序和全部显示, 空列表[] 为全部不显示.
	'dynamic': True,  # 设置是否开启动态菜单, 默认为False. 如果开启, 则会在每次用户登陆时动态展示菜单内容
	'menus': [{
		'app': 'commissionApp',
		'name': '综合信息管理',
		'icon': 'fas fa-code',
		'models': [{
			'name': '定时下载配置信息表',
			'icon': 'fas fa-code',
			'url': 'commissionApp/logdowninfo/',

		}, {
			'name': '设备信息表',
			'icon': 'fas fa-code',
			'url': 'commissionApp/deviceinfo/',

		}, ]
	}, {
		'app': 'djcelery',
		'name': '定时异步任务管理',
		'icon': 'fa fa-file',
		'models': [{
			'name': '定时任务时间格式',
			'url': 'djcelery/crontabschedule/',
			'icon': 'far fa-surprise'
		}, {
			'name': '定时任务',
			'url': 'djcelery/periodictask/',
			'icon': 'fab fa-github'
		},
			{
				'name': '任务结果查询',
				'url': flowerUrl,
				'icon': 'fab fa-github'
			}
		]
	}, {
		'app': 'auth',
		'name': '权限认证',
		'icon': 'fas fa-user-shield',
		'models': [{
			'name': '用户',
			'icon': 'fa fa-user',
			'url': 'auth/user/'
		}, {
			'name': '组',
			'icon': 'fa fa-user',
			'url': 'auth/group/'
		}]
	}]
}





"""{{ project_name }} URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/{{ docs_version }}/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path
from django.conf.urls import include
from commissionApp import api_urls
from django.views.static import serve
from django.conf import settings
# from django.views.generic.base import RedirectView
# favicon_view = RedirectView.as_view(url='/static/images/favicon.ico', permanent=True)



# import xadmin
# from xadmin.plugins import xversion

# xadmin.autodiscover()
# xversion.register_models()

urlpatterns = [
    # re_path(r'^favicon\.ico$', favicon_view),
    path(r'admin/', admin.site.urls),
    # path(r'admin/', xadmin.site.urls),
    path('', include(api_urls)),
	path('static/<path:path>', serve, {'document_root': settings.STATIC_ROOT}),
]


## models.py
# -*-coding:utf-8 -*-
"""
-------------------------------------------------------------------------------
@author  :sdc_os
@time    :2020/02/10
@file    :api_url.py
@desc    :基本的models
@license :(c) Copyright 2020, SDC.
-------------------------------------------------------------------------------
"""
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class AuthToken(Token):
	"""
	name:用户访问Token表
	"""
	started = models.DateTimeField(_("Started"), auto_now_add=True)
	expires = models.DateTimeField(_("Expires"), null=True)


class ProfileUserMetaclass(type):
	"""
	用户元类
	"""
	def __new__(cls, name, bases, attrs):
		if name == 'Model':
			return type.__new__(cls, name, bases, attrs)
		fields = []
		for obj_name, obj in attrs.items():
			if isinstance(obj, models.Field):
				fields.append(obj_name)
			User.add_to_class(obj_name, obj)
		UserAdmin.fieldsets = list(UserAdmin.fieldsets)
		UserAdmin.fieldsets.append((name, {'fields': fields}))
		return type.__new__(cls, name, bases, attrs)


class ProfileUser(object, metaclass=ProfileUserMetaclass):
	GENDER = (
		('M', "男"),
		('W', "女"),
	)
	USER_CATEGORY = (
		('0', '自然人'),
		('1', '系统'),
	)
	department = models.CharField(_("Department"), max_length=255, blank=True, null=True)
	synced = models.DateTimeField(_("Synced"), null=True)
	avatar = models.TextField(_("Avatar"), blank=True, null=True)
	short_name = models.CharField(_("ShortName"), max_length=16, blank=True, null=True)
	sex = models.CharField(_("Sex"), max_length=2, choices=GENDER, blank=True, null=True)
	category = models.CharField(
		_("Category"), max_length=4, choices=USER_CATEGORY, default='0', blank=True, null=True)

	def display_department(self, start_index=1, end_index=3):
		if self.department is None:
			return ""
		else:
			return "\\".join(self.department.split('\\')[start_index:end_index])


class Base(models.Model):
	"""
	基础表，后续的app中models的定义都继承此表
	"""
	creator = models.CharField(verbose_name="创建人用户名", max_length=50, blank=False, null=False, )
	last_mender = models.CharField(verbose_name="最后修改人用户名", max_length=50, blank=False, null=False)
	create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
	last_modified_time = models.DateTimeField(verbose_name="最后修改时间", auto_now=True)

	class Meta:
		abstract = True

#定义模型


# class Student(Base):
# 	name = models.CharField(max_length=20)
# 	sex = models.BooleanField()
# 	contend = models.CharField(max_length=20)
# 	age = models.IntegerField()
# 	isDelete = models.BooleanField(default=False)


class LogDownInfo(Base):
	deviceIp = models.CharField(max_length=200, verbose_name='设备ip段')
	logSavePath = models.CharField(max_length=200, verbose_name='服务器日志保存路径')

	class Meta:
		db_table = 'LogDownInfo'
		verbose_name = '定时下载日志信息表'
		verbose_name_plural = verbose_name


class DeviceInfo(Base):
	deviceIp = models.CharField(max_length=20, verbose_name='设备ip', primary_key=True)
	deviceCatena = models.CharField(max_length=20, verbose_name='产品系列号', default='C')
	sdkName = models.CharField(max_length=20, verbose_name='sdk用户名')
	sdkPass = models.CharField(max_length=20, verbose_name='sdk密码')
	sdkPost = models.CharField(max_length=20, verbose_name='sdk端口号')
	sshName = models.CharField(max_length=20, verbose_name='ssh用户名', null=True, blank=True)
	sshPass = models.CharField(max_length=20, verbose_name='ssh密码', null=True, blank=True)
	sshPost = models.CharField(max_length=20, verbose_name='ssh端口号', null=True, blank=True)
	sftpName = models.CharField(max_length=20, verbose_name='SFTP用户名', null=True, blank=True)
	sftpPass = models.CharField(max_length=20, verbose_name='SFTP密码', null=True, blank=True)
	sftpPost = models.CharField(max_length=20, verbose_name='SFTP端口号', null=True, blank=True)
	sftpPath = models.CharField(max_length=200, verbose_name='sftp绝对路径', null=True, blank=True)
	deviceLogPath = models.CharField(max_length=200, verbose_name='设备日志路径', null=True, blank=True)
	deviceBakLogPath = models.CharField(max_length=200, verbose_name='设备备份日志路径', null=True, blank=True)

	class Meta:
		db_table = 'DeviceInfo'
		verbose_name = '设备信息维护表'
		verbose_name_plural = verbose_name


class BasisInfo(Base):
	projectName = models.CharField(max_length=20, verbose_name='母业务',default='sdc_dingzhi')
	appName = models.CharField(max_length=20, verbose_name='子业务', default='commissionApp')
	key = models.CharField(max_length=20, verbose_name='配置名')
	value = models.CharField(max_length=200, verbose_name='配置值')

	class Meta:
		db_table = 'BasisInfo'
		verbose_name = '基础配置信息表'
		verbose_name_plural = verbose_name



## admin.py
from __future__ import absolute_import, unicode_literals
from django.contrib import admin
# import xadmin
from commissionApp.models import BasisInfo, LogDownInfo, DeviceInfo
# Register your models here.

from djcelery.models import TaskState, WorkerState, PeriodicTask, IntervalSchedule, CrontabSchedule




# 定时下载log信息表注册类
class LogDwonInfoAdmin(admin.ModelAdmin):
	list_display = ('id', 'deviceIp', 'logSavePath',)


# 设备信息维护表
class DeviceInfoAadmin(admin.ModelAdmin):
	list_display = ('deviceIp', 'deviceCatena', 'sdkName', 'sdkPass', 'sdkPost',)


# 基础配置信息表
class BasisInfoAdmin(admin.ModelAdmin):
	list_display = ('projectName', 'appName', 'key', 'value',)


# celery - xadmin
# admin.site.register(IntervalSchedule)  # 存储循环任务设置的时间
# admin.site.register(CrontabSchedule)  # 存储定时任务设置的时间
# admin.site.register(PeriodicTask)  # 存储任务
# admin.site.register(TaskState)  # 存储任务执行状态
# admin.site.register(WorkerState)  # 存储执行任务的worker

# models
admin.site.register(LogDownInfo, LogDwonInfoAdmin)
admin.site.register(DeviceInfo, DeviceInfoAadmin)
admin.site.site_title = "测试定制组后台管理"
admin.site.site_header = "测试定制组"

