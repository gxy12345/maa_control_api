# -*- coding: utf-8 -*-
# @Time    : 2023/11/3 14:35
# @Author  : windoge
# @File    : model.py
# @Software: PyCharm
from typing import Optional
from pydantic import BaseModel


class GetTaskReqItem(BaseModel):
    user: str
    device: str


class SetTaskReqItem(BaseModel):
    user: str
    device: str
    tasks: list
