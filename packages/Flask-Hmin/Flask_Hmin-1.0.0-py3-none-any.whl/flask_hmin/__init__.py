from functools import wraps
from htmlmin import minify


class HMin(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault('HMIN_COMPRESS_HTML', False)

        if app.config['HMIN_COMPRESS_HTML']:
            app.after_request(self.set_response)

    @staticmethod
    def set_response(response):
        if response.content_type == u'text/html; charset=utf-8':
            content = response.data.decode('utf-8')
            compress = minify(content.replace("\n", ""), remove_all_empty_space=True)
            response.set_data(compress)
            return response
        return response

    @staticmethod
    def compress(func):
        @wraps(func)
        def __inner(*a, **k):
            return func(*a, **k)

        return __inner
