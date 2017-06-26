from utils import log
import socket
import urllib.parse
import json
import _thread


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
        header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
        body = json.dumps(self.__dict__, indent=2, ensure_ascii=False)
        # log(body, type(body))
        r = header + '\r\n' + body
        return r.encode(encoding='utf-8')


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


def run(host='', port=5000):
    log('start at {}:{}'.format(host, port))
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))  # 绑定地址，端口
        s.listen(5)  # 最大连接数量
        while True:
            connection, address = s.accept()
            log('connected multithreading', address)
            # 多线程，第一个参数是函数，第二个参数是传给函数的参数，tuple
            _thread.start_new_thread(process_request, (connection,))


if __name__ == '__main__':
    config = dict(
        host='',
        port=5000,
    )
    run(**config)
