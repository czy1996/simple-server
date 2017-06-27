from utils import (template,
                   )


def route_index(request):
    header = 'HTTP/1.1 210 VERY OK\r\nContent-Type: text/html\r\n'
    body = template('index.html', text='shit')
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


route_dict = {
    '/': route_index,

}
