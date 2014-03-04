import os,sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
import web
import json
from server.graph import GraphControl

urls = (
    '/select_gdata','select_gdata',
    '/', 'index',
)

web.config.debug = True
page = web.template.render('static/page/')

class index:
    def GET(self):
        return page.index()
class force_collapsible:
    def GET(self):
        return page.force_collapsible()
class select_gdata:
    def GET(self):
        pass
    def POST(self):
        info = web.input()
        _json = GraphControl().select_gdata(info)
        return json.JSONEncoder().encode(_json)


if __name__ == '__main__':
    app = web.application(urls,globals(),autoreload = True)
    app.run()