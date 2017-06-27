from utils import (template,
                   )


def route_index(request):
    header = 'HTTP/1.1 210 VERY OK\r\nContent-Type: text/html\r\n'
    body = template('index.html', text='shit')
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_static(request):
    filename = request.query.get('file', 'doge.gif')
    path = 'static/' + filename
    with open(path, 'rb') as f:
        header = b'HTTP/1.1 200 OK\r\nContent-Type: image/gif\r\n\r\n'
        img = header + f.read()
        return img

route_dict = {
    '/': route_index,
    '/static': route_static,

}
