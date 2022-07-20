#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from celery_app import celery_app
from celery_once import QueueOnce
import time
import os

@celery_app.task(name="add_longtime", base=QueueOnce, once={"keys": ["b", "a"]})
def add(a, b):
    print("long time task begins")
    # raise Exception("test")
    cmd = "scrapy crawl dytt"
    time.sleep(20)
    print(cmd, "=============")
    os.system(cmd)
    print("long time task ends")
    return a + b