# -*- Mode: Python; coding: utf-8 -*-
from django.apps import AppConfig

default_app_config = 'core.BaseConfig'


class BaseConfig(AppConfig):
    name = 'core'
    verbose_name = u"SISTEMA DE PEDIDOS"
