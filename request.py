from utils import (log, template,
                   )
from routes.routes_index import route_dict as index_routes
from routes.routes_user import route_dict as user_routes
from routes.api_todo import route_dict as todo_api
import urllib.parse
import json

routes_dict = {

}
routes_dict.update(index_routes)
routes_dict.update(user_routes)
routes_dict.update(todo_api)


class Request(object):
    def __init__(self):
        self.method = 'GET'
        self.path = ''
        self.query = {}
        self.body = ''
        self.headers = {}
        self.cookies = {}

    def form(self):
        """
        将 body 解析为字典
        :return:
        """
        args = self.body.split('&')
        f = {}
        for arg in args:
            k, v = arg.split('=')
            f[urllib.parse.unquote(k)] = urllib.parse.unquote(v)
        return f

    def json(self):
        """
        将 body 解析为 json
        :return:
        """
        return json.loads(self.body)

    def parse_raw(self, raw):
        """

        :param raw: String
        :return:
        """
        try:
            self.method = raw.split()[0]
        except IndexError:
            log('Index error', raw.split())
        path = raw.split()[1]
        self.path, self.query = self.parsed_path(path)
        self.body = raw.split('\r\n\r\n', 1)[1]
        self.headers = self.parsed_headers(raw)
        self.cookies = self.parsed_cookies(self.headers)

    @staticmethod
    def parsed_path(path):
        index = path.find('?')
        if index == -1:
            return path, {}
        else:
            path, query_string = path.split('?', 1)
            pairs = query_string.split('&')
            query = {}
            for pair in pairs:
                k, v = pair.split('=')
                query[urllib.parse.unquote(k)] = urllib.parse.unquote(v)
            return path, query

    @staticmethod
    def parsed_headers(raw):
        headers = {}
        headers_string = raw.split('\r\n\r\n', 1)[0].split('\r\n')[1:]
        for h in headers_string:
            headers[h.split(': ')[0]] = h.split(': ')[1]
        return headers

    def response(self):
        method = routes_dict[self.path]
        return method(self)

    @staticmethod
    def parsed_cookies(headers):
        r = {}
        cookies_string = headers.get('Cookie')
        pairs = cookies_string.split('; ')
        for pair in pairs:
            k, v = pair.split('=')
            r[k] = v
        return r


def receive(connection):
    buffer = b''
    while True:
        tmp = connection.recv(1024)
        buffer += tmp
        if len(tmp) < 1024:
            break
    return buffer


def process_request(connection):
    r = receive(connection)
    r = r.decode('utf-8')
    # log('raw', r)
    if len(r.split()) < 2:
        connection.close()
        return  # 傻逼 chrome 空请求
    request = Request()
    request.parse_raw(r)
    log('request', request.__dict__)
    response = request.response()
    connection.sendall(response)
    connection.close()
    log('关闭连接')


"""
*** request {'path': '/favicon.ico',
'query': {},
'method': 'GET',
'body': '',
'cookies': {},
'headers': {'Connection': 'keep-alive',
 'Accept-Encoding': 'gzip, deflate, sdch, br',
 'Host': 'localhost:5000',
 'Referer': 'http://localhost:5000/',
 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
 'Cache-Control': 'no-cache',
 'Pragma': 'no-cache',
 'Accept-Language': 'en-US,en;q=0.8',
 'Cookie': 'Pycharm-7b606eb2=766b5701-f721-4819-a142-f858e9552ab5; _pk_id.100001.1fff=6fdde3af4de92345.1470979320.1.1470979320.1470979320.; __utma=111872281.634963854.1470979320.1470979320.1470979320.1; __utmc=111872281; user=9d2wdafdfdd9dleb', 'Accept': 'image/webp,image/*,*/*;q=0.8'}}

"""
