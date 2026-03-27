mongosh --eval "db.runCommand({ ping: 1 })"
db = MongoConnector({
    "host": "localhost",
    "port": 27017,
    "name": "store",
})