#!/bin/sh
set -e

echo -e "\n ======== \n ${Info} ${GreenBG} 拉取最新项目 ${Font} \n ======== \n"
git pull

echo -e "\n ======== \n ${Info} ${GreenBG} 更新运行依赖 ${Font} \n ======== \n"
pip3 install -r requirements.txt

echo -e "\n ======== \n ${Info} ${GreenBG} 启动MAA Control API ${Font} \n ======== \n"
python ./main.py