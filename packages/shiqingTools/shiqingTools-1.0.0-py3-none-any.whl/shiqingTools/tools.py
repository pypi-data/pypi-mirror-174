#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   tools.py
@Time    :   2022/10/27 15:31:15
@Author  :   shiqing 
@Version :   Cinnamoroll V1
'''
import argparse
import glob
import logging
import os
import pickle as pkl
import time
import urllib
import urllib.request

import colorlog
import numpy as np
import pandas as pd

# 定义不同日志等级颜色
log_colors_config = {
    'DEBUG': 'bold_cyan',
    'INFO': 'bold_green',
    'WARNING': 'bold_yellow',
    'ERROR': 'bold_red',
    'CRITICAL': 'red',
}


class Logger(logging.Logger):
    """
    Usage:
    logger = Logger()
    logger.info(str)
    logger.warning(str)
    """
    def __init__(self, name=None, level='DEBUG', encoding='utf-8'):
        super().__init__(name)
        self.encoding = encoding
        self.level = level
        # 针对所需要的日志信息 手动调整颜色
        formatter = colorlog.ColoredFormatter(
            '%(log_color)s%(asctime)s [%(filename)s:%(''lineno)d] %(log_color)s%(levelname)s:%(message)s',
            reset=True, log_colors=log_colors_config,
            secondary_log_colors={
                'message': {
                    'DEBUG': 'blue',
                    'INFO': 'blue',
                    'WARNING': 'blue',
                    'ERROR': 'red',
                    'CRITICAL': 'bold_red'
                }
            },
            style='%'
        )  # 日志输出格式
        if(name):
            # 创建一个FileHandler，用于写到本地
            rotatingFileHandler = logging.handlers.RotatingFileHandler(filename=self.name,
                                                                       maxBytes=1024 * 1024 * 50,
                                                                       backupCount=5)
            rotatingFileHandler.setFormatter(
                logging.Formatter('%(asctime)s [%(filename)s:%(''lineno)d] %(levelname)s:%(message)s'))
            rotatingFileHandler.setLevel(logging.DEBUG)
            self.addHandler(rotatingFileHandler)
        # 创建一个StreamHandler,用于输出到控制台
        console = colorlog.StreamHandler()
        console.setLevel(logging.DEBUG)
        console.setFormatter(formatter)
        self.addHandler(console)
        self.setLevel(logging.DEBUG)


def count_time(func):
    """ decrator to count function execution time
    """
    def wrapper(*args, **kwargs):
        begin = time.time()
        func(*args, **kwargs)
        end = time.time()
        print("耗时:%s" % (end-begin))

    return wrapper


def download_image(img_path: str, img_url: str) -> int:
    """downlowad image from img_url

    Args:
        img_path (str): image path
        img_url (str): image url

    Returns:
        int: return 1 if download successfully else 0
    """
    try:
        if not os.path.exists(img_path):
            request = urllib.request.Request(img_url)
            response = urllib.request.urlopen(request)
            get_img = response.read()
            with open(img_path, 'wb') as fp:
                fp.write(get_img)
    except:
        return 0

    return 1


