from jinja2 import Environment, FileSystemLoader
import os.path


def log(*args, **kwargs):
    print('***', *args, **kwargs)

# def log(*args, **kwargs):
#     # time.time() 返回 unix time
#     # 如何把 unix time 转换为普通人类可以看懂的格式呢？
#     format = '%H:%M:%S'
#     value = time.localtime(int(time.time()))
#     dt = time.strftime(format, value)
#     with open('log.txt', 'a', encoding='utf-8') as f:
#         print(dt, *args, file=f, **kwargs)


path = '{}/templates/'.format(os.path.dirname(__file__))
loader = FileSystemLoader(path)
env = Environment(loader=loader)


def template(path, **kwargs):
    """
    接收路径和参数，返回 html
    :param path:
    :param kwargs:
    :return:
    """
    t = env.get_template(path)
    return t.render(**kwargs)
