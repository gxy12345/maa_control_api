# -*- coding: utf-8 -*-
# @Time    : 2023/11/3 14:27
# @Author  : windoge
# @File    : get_task.py
# @Software: PyCharm
import uuid
import json
import logging
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from maa.model import GetTaskReqItem, SetTaskReqItem, ReportTaskReqItem
from maa.get_task import create_user, get_tasks, set_tasks, report_task_item
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
        user_info['device'] = item.device
        user_info['tasks'] = await get_tasks(item)

    return user_info


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

    print("MAA Control API Server V0.1")
    print("By Windoge")

    with open('config/config.yaml') as f:
        config = yaml.load(f, yaml.FullLoader)

    host = config['api'].get('host', '0.0.0.0')
    port = config['api'].get('port', 8088)

    uvicorn.run(app, host=host, port=port)
