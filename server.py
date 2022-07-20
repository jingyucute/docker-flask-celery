#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
from flask import Flask, request, redirect

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>It works!</h1>"

@app.route("/get_top_movies", methods=['GET', 'POST'])
def get_douban_top_movie():
    cmd = "scrapy crawl douban_top_movie"
    os.system(cmd)
    return {
        "status": "success",
        "data": "nb"
    }

