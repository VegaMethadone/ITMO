import os
from build import TargetDir, LabPrefix
import matplotlib.pyplot as plt


def  run(target: TargetDir, prefix: LabPrefix, core: str, size: int):

    N = size / 100
    n_size = [N + N * i for i in range(101)]
    print(n_size)
           
    time_array = []
    for i in range(len(n_size)):
        liba = 'LD_LIBRARY_PATH="$PWD/FW_1.3.1_Lin64/lib"'
        path = f'{liba} ./{TargetDir.CLANG}/{LabPrefix.DEFAULT} {n_size[i]} {core}'
        print(path)
        result = os.popen(path).read()
        nums, exectime = result.split('\n')[:2]
        print("Exectime: ", exectime)
        
        time_array.append(int(exectime))
        print("Array: ", time_array)

    return n_size, time_array

def main():
    x, y = run(TargetDir.CLANG, LabPrefix.DEFAULT, '8', 500)
    graph(x, y)

def graph(x, y):
    plt.plot(x, y)
    plt.xlabel('n_size')
    plt.ylabel('exec ms')
    plt.savefig('./assets/parallel.png')
    plt.clf()

if __name__ == '__main__':
    main()