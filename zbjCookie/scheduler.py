# -*- coding: utf-8 -*-
import sched
import time
from zbjCookie.log import Logger
from zbjCookie.operatingRedis import update_single_cookie
from zbjCookie.autoCookies import all_cookie, single_cookie


logger = Logger(filename='./log/scheduler.log')
ALL_U_DATA = [000000, 111111]  # 全部账号
ALL_U_TIME = 600  # 更新全部cookie时间，间隔600s
SINGLE_U_TIME = 120  # 更新单个cookie时间
s = sched.scheduler(time.time, time.sleep)


def scheduler_all():
    """
    更新全部cookie
    :return:
    """
    logger.warning('[scheduler_all] scheduled task start :(')
    # delete_data()
    # logger.warning('[redis] clear redis data')
    all_cookie(ALL_U_DATA)
    logger.warning('[scheduler_all] scheduled task stop :)')
    logger.info('------------:)------------')


def scheduler_single():
    """
    更新单个cookie
    :return:
    """
    logger.warning('[scheduler_single] scheduled task start :(')
    u = update_single_cookie()
    if u:
        single_cookie(u)
        logger.warning('[scheduler_single] scheduled task stop :(')
    else:logger.warning('[scheduler_single] no task running :(')
    logger.info('------------:)------------')


if __name__ == '__main__':
    while 1:
        for number in range(2):  # 执行两次更新单个cookie操作
            s.enter(SINGLE_U_TIME, 1, scheduler_single, ())
        s.enter(ALL_U_TIME, 0, scheduler_all, ())
        s.run()
