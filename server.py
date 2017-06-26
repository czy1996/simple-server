from utils import log
import socket


class Request(object):
    pass


def receive(connection):
    buffer = []
    while True:
        tmp = connection.recv(1024)
        if tmp:
            buffer.append(tmp)
        else:
            break
    return b''.join(buffer)


request = Request()


def run(host='', port=5000):
    log('start at {}:{}'.format(host, port))
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))  # 绑定地址，端口
        s.listen(5)  # 最大连接数量
        while True:
            connection, address = s.accept()
            r = receive(connection)
            r = r.decode('utf-8')
            log('raw', r)
            if len(r.split()) < 2:
                continue
            # request.parse_raw(r)
            # response = request.response()
            # connection.sendall(response)
            connection.close()


if __name__ == '__main__':
    config = dict(
        host='',
        port=5000,
    )
    run(**config)