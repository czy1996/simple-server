from utils import log
from request import process_request
import socket
import _thread


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
