#PLAYGROUND TO TEST
from Backend.microservices.app.API.v1.db.mongodb.database import personal

service_raw_v = personal.find_one({ "version": "v3" })
print(service_raw_v)