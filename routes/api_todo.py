from models.todo import Todo
from utils import (json_response,
                   )


def todo_all(request):
    todo_list = Todo.all()
    todos = [t.json() for t in todo_list]
    return json_response(todos)


def todo_add(request):
    form = request.json()
    t = Todo.new(form)
    return json_response(t.json())


def todo_delete(request):
    """
    /delete?id=1
    :param request:
    :return:
    """
    todo_id = int(request.query.get('id'))
    t = Todo.delete(todo_id)
    return json_response(t.json())


def todo_update(request):
    form = request.json()
    todo_id = int(form.get('id'))
    t = Todo.update(todo_id, form)
    return json_response(t.json())


route_dict = {
    '/api/todo/all': todo_all,
    '/api/todo/add': todo_add,
    '/api/todo/delete': todo_delete,
    '/api/todo/update': todo_update,
}
