import time
import multiprocessing
from connection import MongoClient
from faker import Faker
from pymongo.errors import ConnectionFailure


def add_data():
    fake = Faker()
    port = "27017"
    client = MongoClient(port)

   # try:
    while True:
        start = time.time()
        try:
            document = {
                "Name": fake.name(),
                "Age": fake.random_int(min=18, max=80),
                "Country": fake.country(),
                "Address": fake.address()
            }
            res = client.insert_one(document)
            end = time.time()
            print("Inserted index:", res.inserted_id, "Recording time: ", end - start)           
            if end - start > 3.0:
                print("Mongo is dead")
                return    
        except ConnectionFailure:
            print("MongoDB is dead")
            return

    #except KeyboardInterrupt:
        #pass

def add_data_proc():
    num_processors = 6
    processes = []

    for _ in range(num_processors):
        process = multiprocessing.Process(target=add_data)
        process.start()
        processes.append(process)

    for process in processes:
        process.join()



