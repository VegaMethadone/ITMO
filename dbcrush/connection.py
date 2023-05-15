import pymongo

def MongoClient(port):
    try:
        if port == "27017":
            client = pymongo.MongoClient(f"mongodb://localhost:{port}/")
        else:
            client = pymongo.MongoClient(f"mongodb://localhost:{port}/?readPreference=secondary")
        db = client["lab"]
        users_collection = db["lol"]
        print(users_collection)
        return users_collection
    except pymongo.errors.ConnectionError as e:
        print("Error connecting to MongoDB:", e)
        return None


