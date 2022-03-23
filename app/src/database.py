import pymongo
class DB(object):
    URI = "mongodb://localhost:27017/vovid-uk"
     
    @staticmethod
    def init():
        client = pymongo.MongoClient(DB.URI)
        DB.DATABASE = client['vovid-uk']

    @staticmethod
    def insert(collection, data):
        DB.DATABASE[collection].insert(data)