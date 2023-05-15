from add import add_data_proc
from read import crush_db2, crush_db3
import time


def main():
    star = time.time()
    add_data_proc()
    end_add = time.time()
    crush_db2()
    end_read_2 = time.time()
    crush_db3
    end_read_3 = time.time()
    print("Node 1 died at: ", end_add - star, "\nNode 2 died at: ", end_read_2 - star, "\nNode 3 died at: ", end_read_3 - star)

if __name__ == '__main__':
    main()


