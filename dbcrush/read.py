import time
from connection import MongoClient
import multiprocessing
from pymongo.errors import ServerSelectionTimeoutError



def read_db2():
    port = "27018" 
    users_collection = MongoClient(port)
    try:
        for cursor in users_collection.find():
            start = time.time()
            print(cursor)
            end = time.time()
            print("Reading time: ", end - start)
            if end - start > 3.0:
                print(f"Mongo is dead with port {port} is dead")
                return  
    except ServerSelectionTimeoutError as err:
        print(f"MongoDb with port: {port} is dead. Reason is: ", err)
        return

def read_db3():
    port = "27019" 
    users_collection = MongoClient(port)
    try:
        for cursor in users_collection.find():
            start = time.time()
            print(cursor)
            end = time.time()
            print("Reading time: ", end - start)
            if end - start > 3.0:
                print(f"Mongo is dead with port {port} is dead")
                return  
    except ServerSelectionTimeoutError as err:
        print(f"MongoDb with port: {port} is dead. Reason is: ", err)
        return


def crush_db2():
    num_processors = 6
    processes = []

    for _ in range(num_processors):
        process = multiprocessing.Process(target=read_db2)
        process.start()
        processes.append(process)

    for process in processes:
        process.join()

def crush_db3():
    num_processors = 6
    processes = []

    for _ in range(num_processors):
        process = multiprocessing.Process(target=read_db3)
        process.start()
        processes.append(process)

    for process in processes:
        process.join()


