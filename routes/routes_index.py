from utils import (template, html_response, current_user, redirect
                   )
from models.user import User


def route_index(request):
    uid = current_user(request)
    u = User.find_by(id=uid)
    if u is not None:
        username = u.username
    else:
        username = '游客'
    return html_response('index.html', username=username)


def route_static(request):
    filename = request.query.get('file', 'doge.gif')
    path = 'static/' + filename
    with open(path, 'rb') as f:
        header = b'HTTP/1.1 200 OK\r\nContent-Type: image/gif\r\n\r\n'
        img = header + f.read()
        return img


def route_fav(request):
    return redirect('/static?file=闪电侠.jpg')


route_dict = {
    '/': route_index,
    '/static': route_static,
    '/favicon.ico': route_fav,

}
