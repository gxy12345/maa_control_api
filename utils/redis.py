# -*- coding: utf-8 -*-
# @Time    : 2023/11/3 15:10
# @Author  : windoge
# @File    : redis.py
# @Software: PyCharm
import aioredis

redis = aioredis.from_url("redis://localhost")


async def get(key):
    value = await redis.get(key)
    return value


async def set(key, value, ex=None):
    await redis.set(key, value, ex)


