# -*- coding: utf-8 -*-
# @Time    : 2023/11/3 14:27
# @Author  : windoge
# @File    : get_task.py
# @Software: PyCharm
import uuid
import json
import logging
from fastapi import FastAPI, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from maa.model import GetTaskReqItem, SetTaskReqItem, ReportTaskReqItem
from maa.get_task import create_user, get_tasks, set_tasks, report_task_item, update_user
from maa.constant import USER_KEY_PREFIX
from utils import redis

app = FastAPI()

mock_json = {
    "tasks": []
}


@app.post("/maa/get_task")
async def get_task(item: GetTaskReqItem):
    print(item.user)
    user = await redis.get(f'{USER_KEY_PREFIX}{item.user}')
    print(user)
    if not user:
        user_info = await create_user(item)
        return user_info
    else:
        user_info = json.loads(user)
        user_info['tasks'] = await get_tasks(item)
        if user_info['device'] != item.device:
            user_info['device'] = item.device
            await update_user(item.user, user_info)

    return user_info


@app.get("/maa/check_user")
async def get_task(user: str, device: str):
    print(user)
    print(device)
    user_str = await redis.get(f'{USER_KEY_PREFIX}{user}')
    if not user_str:
        return {"result": False}
    else:
        user_info = json.loads(user_str)
        if not user_info['device'] == device:
            return {"result": False}
    return {"result": True}


@app.get("/maa/get_device")
async def get_task(user: str):
    user_str = await redis.get(f'{USER_KEY_PREFIX}{user}')
    if not user_str:
        return {"device": None}
    else:
        user_info = json.loads(user_str)
        return {"result": user_info.get('device')}


@app.post("/maa/set_task")
async def set_task(item: SetTaskReqItem):
    user = await redis.get(f'{USER_KEY_PREFIX}{item.user}')
    print(user)
    if not user:
        return JSONResponse({"err_msg": "cannot find user"}, status_code=400)
    else:
        task_list = await set_tasks(item)

    return {"tasks": task_list}


@app.post("/maa/report_task")
async def report_task(item: ReportTaskReqItem):
    user = await redis.get(f'{USER_KEY_PREFIX}{item.user}')
    print(user)
    if not user:
        return JSONResponse({"err_msg": "cannot find user"}, status_code=400)
    else:
        await report_task_item(item)


if __name__ == "__main__":
    import uvicorn
    import yaml
    import os

    print("MAA Control API Server V0.1")
    print("By Windoge")

    with open('config/config.yaml') as f:
        config = yaml.load(f, yaml.FullLoader)

    host = config['api'].get('host', '0.0.0.0')
    port = config['api'].get('port', 8088)
    cert_path = config['ssl'].get('cert_path')
    key_path = config['ssl'].get('key_path')

    if cert_path and key_path and os.path.exists(cert_path) and os.path.exists(key_path):
        uvicorn.run(app, host=host, port=port, ssl_keyfile=key_path, ssl_certfile=cert_path)
    else:
        uvicorn.run(app, host=host, port=port)
