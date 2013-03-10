# -*- coding: utf-8 -*-

DEBUG = True
CELERY_BROKER_URL = 'amqp://guest@localhost//'

try:
    from local_settings import *
except ImportError:
    pass