#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   qbit_down_aps.py
@Time    :   2023/11/04 15:21:37
@Author  :   leanfly
@Version :   1.0
@Contact :   ningmuyu@live.com
@Desc    :   当前文件作用
'''


from fastapi import FastAPI,responses
from apscheduler.schedulers.background import BackgroundScheduler
import uvicorn
import qbittorrentapi
from loguru import logger
import requests
import re
import yaml
from urllib.parse import urlparse
import os
import base64


## 指定配置文件路径 ##
config_path = "/code/config.yaml"

## 指定种子文件的URL ##
torrent_page = "aHR0cHM6Ly9vbmVqYXYuY29tL3BvcHVsYXIvP2phdj0x"
days = 7

## 配置qbit ##
qbit_conn = dict(
    host="http://172.17.0.1",
    port=7777,
    username="admin",
    password="adminadmin",
)


## 获取本地配置文件的配置信息 ##
if os.path.exists(config_path):
    with open(config_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
        
        qbit_conn = dict(
            host=data["qbit"]["host"],
            port=data["qbit"]["port"],
            username=data["qbit"]["username"],
            password=data["qbit"]["password"],
        )

        torrent_page = data["torrents_page"]
        days = data["days"]

## 判断是否 base64 处理过 ##
def is_base64(data):
    try:
        base64.b64decode(data)
        return True
    except:
        return False


def get_tottents(url)->list:
    url = base64.b64decode(url).decode("utf-8") if is_base64(url) else url
    url_data = urlparse(url)
    shceme = url_data.scheme
    hostname = url_data.hostname
    
    with requests.get(url) as req:
        if req.status_code != 200:
            return

        res = req.text
        res = re.sub(r"\n|\r|\t", "", res)
        
        torrents = re.findall(r'<a class="button is-primary is-fullwidth" data-toggle="tooltip" title="Download .torrent" target="_blank" href="(.*?)" rel="nofollow">', res)
        torrents = [f"{shceme}://{hostname}{i}" for i in torrents]
        return torrents


def add_qbit_task(url: str):
    qbt_client = qbittorrentapi.Client(**qbit_conn)
    try:
        qbt_client.auth_log_in()
        # logger.info(qbt_client.app_build_info())

        # 获取全部种子信息
        # hash_list = [tr.hash for tr in qbt_client.torrents.info()]
        qbt_client.torrents.add(urls=url, save_path="/downloads", category="")

    except:
        pass


def main_handle():
    torrents = get_tottents()
    if torrents:
        for i in torrents:
            add_qbit_task(i)



scheduler = BackgroundScheduler()
scheduler.add_job(
    main_handle,
    "interval",
    days=days,
)

app = FastAPI()

@app.on_event("startup")
def app_start():
    logger.info("定时任务已启动")
    scheduler.start()
    jobs = scheduler.get_jobs()
    
    logger.info(jobs[0])
    
    
@app.on_event("shutdown")
def app_shutdown():
    logger.info("定时任务已关闭")
    scheduler.shutdown()


@app.get("/jobs")
def get_jobs():
    jobs = scheduler.get_jobs()
    job_lst = [job for job in jobs]
    
    return responses.JSONResponse(content=job_lst)

if __name__ == "__main__":
    uvicorn.run(app="app:app", host="0.0.0.0", port=44444)
