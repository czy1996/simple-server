from utils import (template, html_response, redirect, random_str, log,
                   )
from models.user import User
from routes.session import session


def route_login(request):
    headers = {
        'Content-Type': 'text/html',
    }
    if request.method == 'POST':
        form = request.form()
        u = User(form)
        if u.validate_login():
            user = User.find_by(username=u.username)
            session_id = random_str()
            session[session_id] = user.id
            headers['Set-Cookie'] = 'user={}'.format(session_id)
            return redirect('/', headers)
    return html_response('login.html')


def route_register(request):
    if request.method == 'POST':
        form = request.form()
        u = User(form)
        if u.validate_register() is not None:
            log('注册成功', u)
            return redirect('/login')
        else:
            return redirect('/register')
    return html_response('register.html')


route_dict = {
    '/login': route_login,
    '/register': route_register,

}
