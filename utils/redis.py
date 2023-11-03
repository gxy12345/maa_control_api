# -*- coding: utf-8 -*-
# @Time    : 2023/11/3 15:10
# @Author  : windoge
# @File    : redis.py
# @Software: PyCharm
import aioredis
import yaml

with open('config/config.yaml') as f:
    config = yaml.load(f, yaml.FullLoader)

if config.get('redis'):
    host = config['redis'].get('host', 'localhost')
    port = config['redis'].get('port', 6379)
    password = config['redis'].get('password')
else:
    host = 'localhost'
    port = 6379
    password = None


if password:
    redis = aioredis.from_url(f"redis://{password}@{host}:{port}")
else:
    redis = aioredis.from_url(f"redis://{host}:{port}")


async def get(key):
    value = await redis.get(key)
    return value


async def set(key, value, ex=None):
    await redis.set(key, value, ex)


