from jinja2 import Environment, FileSystemLoader
from routes.session import session
import os.path
import random
import time
import json


# def log(*args, **kwargs):
#     print('***', *args, **kwargs)


def log(*args, **kwargs):
    # time.time() 返回 unix time
    # 如何把 unix time 转换为普通人类可以看懂的格式呢？
    format = '%H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    with open('log.txt', 'a', encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)


path = '{}/templates/'.format(os.path.dirname(__file__))
loader = FileSystemLoader(path)
env = Environment(loader=loader)


def template(path, **kwargs):
    """
    接收路径和参数，返回 html
    :param path:
    :param kwargs:
    :return:
    """
    t = env.get_template(path)
    return t.render(**kwargs)


def html_response(path, **kwargs):
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    body = template(path, **kwargs)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def random_str():
    seed = 'abcdefjsad89234hdsfkljasdkjghigaksldf89weru'
    s = ''
    for i in range(16):
        random_index = random.randint(0, len(seed) - 2)
        s += seed[random_index]
    return s


def response_with_headers(headers, status_code=200):
    """
    Content-Type: text/html
    Set-Cookie: user=gua
    """
    header = 'HTTP/1.1 {} VERY OK\r\n'.format(status_code)
    header += ''.join(['{}: {}\r\n'.format(k, v)
                       for k, v in headers.items()])
    return header


def redirect(location, headers=None):
    if headers is None:
        headers = {
            'Content-Type': 'text/html',
        }
    headers['Location'] = location
    # 302 状态码的含义, Location 的作用
    header = response_with_headers(headers, 302)
    r = header + '\r\n' + ''
    return r.encode(encoding='utf-8')


def current_user(request):
    session_id = request.cookies.get('user', '')
    uid = session.get(session_id, -1)
    return uid


def json_response(data):
    """
    json 响应
    """
    # 注意, content-type 现在是 application/json 而不是 text/html
    # 这个不是很要紧, 因为客户端可以忽略这个
    header = 'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n'
    # json.dumps 用于把 list 或者 dict 转化为 json 格式的字符串
    # ensure_ascii=False 可以正确处理中文
    # indent=2 表示格式化缩进, 方便好看用的
    body = json.dumps(data, ensure_ascii=False, indent=2)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')
