from Backend.microservices.app.API.v1.tornado_.base import BaseHandler
from tornado import gen

class BookingCard(BaseHandler):
    @gen.coroutine
    def get(self):
        feed = yield self.db.table("table").changes().run(self.db)
        changes = []
        while (yield feed.fetch_next()):
            change = yield feed.next()
            changes.append(change)
        self.write({"changes": changes})
