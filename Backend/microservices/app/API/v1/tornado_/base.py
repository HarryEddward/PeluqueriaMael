import tornado.web

class BaseHandler(tornado.web.RequestHandler):
    def initialize(self, db):
        self.db = db
