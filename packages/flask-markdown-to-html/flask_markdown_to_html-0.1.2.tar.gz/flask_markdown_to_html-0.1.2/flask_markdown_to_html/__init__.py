from markdown import markdown

from flask import*


class flask_markdown_to_html(object):
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):

       
        app.extensions['md'] = self
        app.jinja_env.globals['md'] = self
        
    @staticmethod
    def markdown_to_html(word):
        word=markdown(word,extensions=['markdown.extensions.extra',
        'markdown.extensions.codehilite', #代码高亮扩展
        'markdown.extensions.toc',
        'markdown.extensions.tables',
        'markdown.extensions.fenced_code'])
        return Markup(word)
        

    def render_markdown(self,name):
        path="../static/markdown"
        with open(f'{path}/{name}',"r",encoding="utf-8") as md:
            word=md.read()
            md.close
        word=markdown(word,extensions=['markdown.extensions.extra',
                'markdown.extensions.codehilite', #代码高亮扩展
                'markdown.extensions.toc',
                'markdown.extensions.tables',
                'markdown.extensions.fenced_code'])
        return Markup(f"{word}")