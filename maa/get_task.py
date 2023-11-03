# -*- coding: utf-8 -*-
# @Time    : 2023/11/3 14:27
# @Author  : windoge
# @File    : get_task.py
# @Software: PyCharm
import uuid
import json
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from maa.model import GetTaskReqItem, SetTaskReqItem
from maa.constant import USER_KEY_PREFIX, TASK_KEY_PREFIX, TASK_TYPE_ENUM
from utils import redis


async def create_user(item: GetTaskReqItem):
    print("create_new_user")
    user_info = {
        "uid": str(uuid.uuid1()),
        "device": item.device,
        "tasks": []
    }
    await redis.set(f'{USER_KEY_PREFIX}{item.user}', json.dumps(user_info))
    return user_info


async def get_tasks(item: GetTaskReqItem):
    print("get existed task")
    task_info = await redis.get(f'{TASK_KEY_PREFIX}{item.user}:{item.device}')
    if not task_info:
        return []
    return json.loads(task_info)


async def set_tasks(item: SetTaskReqItem):
    task_list = []
    for task in item.tasks:
        task_type = task.get('type')
        if task_type not in TASK_TYPE_ENUM:
            continue
        task_item = {
            "id": str(uuid.uuid1()),
            "type": task_type
        }
        task_list.append(task_item)
    await redis.set(f'{TASK_KEY_PREFIX}{item.user}:{item.device}', json.dumps(task_list))
    return task_list
