# -*-coding=utf-8-*-
# @Time : 2018/8/8 22:23
# @File : run.py
from scrapy import cmdline
cmd ='scrapy crawl jd_book'
cmdline.execute(cmd.split())