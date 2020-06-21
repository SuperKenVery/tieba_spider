# -*- coding: UTF-8 -*-
__author__ = 'Chengrongkai'

import time
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from feiyan_spider import VirusSupervise

# 错误监控
def my_listener(event):
    if event.exception:
        print ('任务出错了！！！！！！')
    else:
        print ('任务照常运行...')
# 爬取文章
def feiyan_spider():
    print("开始采集:{}".format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
    vs = VirusSupervise()
    vs.filtration_data()

# 任务
def start():
    print('创建任务')
    #创建调度器：BlockingScheduler
    scheduler = BlockingScheduler()
    scheduler.add_listener(my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    # 添加文章爬取的定时任务：每天的早上7点执行
    scheduler.add_job(feiyan_spider, 'cron', hour=8, minute=10)
    scheduler.start()


if __name__ == "__main__":
    start()



