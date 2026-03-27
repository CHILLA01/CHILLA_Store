import pymongo

# def create_uri(config):
#     username = config.get("username")
#     password = config.get("password")

#     credentials = f"{username}:{password}@" if username and password else ""

#     return "mongodb://{credentials}{host}:{port}/{name}".format(
#         credentials=credentials, **config
#     )

class MongoConnector:

    def __init__(self, config):
        # uri = create_uri(config)
        self.client = pymongo.MongoClient("localhost:27017")
        self._db = self.client[config["name"]]

    def check_database_exists(self, database_name):
        return database_name in self.client.list_database_names()

    def check_collection_exists(self, collection_name):
        return collection_name in self._db.list_collection_names()

    def insert_one(self, collection, document):
        return self._db[collection].insert_one(document)

    def insert_many(self, collection, documents):
        return self._db[collection].insert_many(documents)

    def find(self, collection, query, sort=None, asc=1):
        data = self._db[collection].find(query)
        if sort:
            data = data.sort(sort, asc)
        return data

    def delete_one(self, collection, query):
        return self._db[collection].delete_one(query)

    def delete_many(self, collection, query):
        return self._db[collection].delete_many(query)

    def drop(self, collection):
        return self._db[collection].drop()

    def update_one(self, collection, query, data):
        return self._db[collection].update_one(query, data)

    def update_many(self, collection, query, data):
        return self._db[collection].update_many(query, data)