import tornado.web

class MainRequestHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")
