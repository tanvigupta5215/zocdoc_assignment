import pymongo


class DBConnector:
    db_instance = None

    @staticmethod
    def connect_db():
        client = pymongo.MongoClient("localhost", 27017)
        DBConnector.db_instance = client.zocdoc
        DBConnector.db_instance.movies.drop()

    @staticmethod
    def get_db():
        if DBConnector.db_instance is None:
            DBConnector.connect_db()
        return DBConnector.db_instance

    @staticmethod
    def insert_many(data):
        db = DBConnector.get_db()
        movies_collection = db.movies
        movies_collection.insert_many(data)
