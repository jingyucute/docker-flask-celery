#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from celery import Celery, platforms
from kombu import Queue, Exchange
import base_config

platforms.C_FORCE_ROOT = True

class CeleryConfig:
    enable_utc = True
    # 任务队列的链接地址
    broker_url = 'redis://{REDIS_HOST}:{REDIS_PORT}'.format(
        REDIS_HOST=base_config.REDIS_HOST, 
        REDIS_PORT=base_config.REDIS_PORT
    )
    # 结果队列的链接地址
    result_backend = 'mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}?authSource={MONGO_DB}'.format(
        MONGO_USER=base_config.MONGO_USER, 
        MONGO_PASSWORD=base_config.MONGO_PASSWORD, 
        MONGO_HOST=base_config.MONGO_HOST, 
        MONGO_PORT=base_config.MONGO_PORT, 
        MONGO_DB=base_config.MONGO_DB
    )

    timezone = "Asia/Shanghai"

    # 配置ONCE,
    # 这里的backend 和 上面的backend 有区别， 这里主要是利用redis来实现分布式锁
    ONCE = {
        'backend': 'celery_once.backends.Redis',
        'settings': {
            'url': "redis://{REDIS_HOST}:{REDIS_PORT}/1".format(
                    REDIS_HOST=base_config.REDIS_HOST, 
                    REDIS_PORT=base_config.REDIS_PORT
                ) ,
            'default_timeout': 60 * 60
        }
    }


celery_app = Celery(__name__)
celery_app.config_from_object(CeleryConfig)
celery_app.conf.include = [
    "celery_tasks.tasks"
]

