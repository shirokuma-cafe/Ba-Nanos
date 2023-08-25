from pymongo.mongo_client import MongoClient
#from dotenv import dotenv_values
#conf = dotenv_values("../../.env")

class CollectionManager():
    """Class to handle accessing various collections inside MongoDB
    :param uri: string containing mongoDB connectiong string.
    """
    def __init__(self, uri) -> None:
        self.uri = uri

    def get_styles_collection(self):

        self.client = MongoClient(self.uri)
        try:
        # Fetches collection based on given parameters (database, name)
            db = self.client["styles"]
            collection = db["image_styles"]

        except Exception as e:
            print(e)

        return collection

    def get_user_collection(self, database="user", collection_name="user_data"):
        self.client = MongoClient(self.uri)
        try:
        # Fetches collection based on given parameters (database, name)
            db = self.client[database]
            collection = db[collection_name]

        except Exception as e:
            print(e)

        return collection

# Returns a collection with the specified collection name
"""
def get_collection(database: str, collection_name: str):
    # Create a new client and connect to the server
    client = MongoClient(URI)
    try:
        # Fetches collection based on given parameters (database, name)
        db = client[database]
        collection = db[collection_name]

    except Exception as e:
        print(e)

    return collection
"""