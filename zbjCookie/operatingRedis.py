# -*- coding: utf-8 -*-

import redis

u_data = [0000000, 11111111]  # 帐号


_redis_conn = redis.Redis(host='xxx.xxx.xxx.xxx', port=6379, db=0)


def _hset_data(u_data):
    """
    查询是否有cookie，是否已被使用
    :return:
    """
    for u in u_data:
        used_status = int(_redis_conn.hget(str(u), 'usedStatus').decode('utf-8'))
        if used_status == 0:
            _redis_conn.hset(str(u), 'usedStatus', 1)  # 更新cookie状态
            return _redis_conn.hget(str(u), 'cookie').decode('utf-8')
        else:
            continue
    return False


def update_status():
    """
    更新cookie状态
    :return:
    """
    for u in u_data:
        _redis_conn.hset(str(u), 'usedStatus', '0')


def delete_data():
    """
    清空数据库
    :return:
    """
    for u in u_data:
        str_u = str(u)
        _redis_conn.delete(str_u)


def dict_to_json(data):
    """
    将字典转换成json（[{},{}]）
    :return:
    """
    import json
    old_d = json.loads(data)
    new_d_list = []
    for old_k, old_v in old_d.items():
        new_d = dict()
        new_d['name'] = old_k
        new_d['value'] = old_v
        new_d_list.append(new_d)
    new_d_json = json.dumps(new_d_list)
    return new_d_json


def get_single_cookie():
    """
    获取一个cookie
    :return:
    """
    for u in u_data:
        if _redis_conn.hget(str(u), 'usedStatus').decode('utf8') == '1':
            if _redis_conn.hget(str(u), 'isUsingStatus').decode('utf8') == '1':  # 获取已被用户使用的cookie
                _redis_conn.hset(str(u), 'isUsingStatus', '0')  # 清除正在使用的状态
    for u in u_data:
        if _redis_conn.hget(str(u), 'usedStatus').decode('utf8') != '1':
            import json
            _redis_conn.hset(str(u), 'usedStatus', '1')
            _redis_conn.hset(str(u), 'isUsingStatus', '1')  # 当前cookie正在使用
            cookie_bytes = _redis_conn.hget(str(u), 'cookie').decode('utf-8')
            cookie_res = dict_to_json(cookie_bytes)
            return cookie_res
    return '{"message": "no cookie"}'


def update_single_cookie():
    """
    查询需要更新cookie的u
    :return:
    """
    for u in u_data[::-1]:
        if _redis_conn.hget(str(u), 'usedStatus').decode('utf8') == '1':  # 被使用过
            if _redis_conn.hget(str(u), 'isUsingStatus').decode('utf8') == '0':  # 避开cookie正在被使用
                return str(u)
        return None
