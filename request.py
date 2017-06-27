from utils import (log, template,
                   )
from routes.routes_index import route_dict as index_routes
import urllib.parse
import json

routes_dict = {

}
routes_dict.update(index_routes)


class Request(object):
    def __init__(self):
        self.method = 'GET'
        self.path = ''
        self.query = {}
        self.body = ''
        self.headers = {}

    def form(self):
        """
        将 body 解析为字典
        :return:
        """
        pass

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
    # log('request', request.__dict__)
    response = request.response()
    connection.sendall(response)
    connection.close()
    log('关闭连接')
