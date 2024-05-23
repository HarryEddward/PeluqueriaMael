import tornado.ioloop
import tornado.web
from Backend.microservices.app.API.v1.tornado_.db.database import db_connection
from Backend.microservices.app.API.v1.tornado_.routes.public.booking_card import BookingCard

def make_app():

    v = "v1"

    pb = f"/app/api/{v}/worker/ws/public"
    pr = f"/app/api/{v}/worker/ws/restricted"

    return tornado.web.Application([
        (fr"{pb}/booking_card", BookingCard, dict(db=db_connection)),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
