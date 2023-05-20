import os
import json
from build import TargetDir, LabPrefix
import matplotlib.pyplot as plt


def n_variation():
    with open('./assets/n_config.json') as asset:
        data = json.load(asset)
        N1 = data['CLANG']['1000']
        N2 = data['CLANG']['5000']
        N = N2 - N1
        N //= 10
    res = [N1 + N * i for i in range(10)]
    return res
        

def run(target: TargetDir, cores: str, data):
    lab_name = LabPrefix.N_THREADS
    options = ''
    if cores == '0':
        lab_name = LabPrefix.NO_PARALLEL
    else:
        options = f'OMP_NUM_THREADS={cores} OMP_DYNAMIC=FALSE '
    res = []
    for i in range(10):
        print(f'{options}./{target.value}/{lab_name} {data[i]} {cores}')
        result = os.popen(f'{options}./{target.value}/{lab_name} {data[i]} {cores}').read()
        if cores == '0':
            _, timing = result.split("\n")[:2]
        else:
            timing = result.split("\n")
            print(timing)
            timing, _ = timing[len(timing) - 2:]
        res.append(int(timing))
        print(res)
    return res

def graph_parallel(arr, data):
    
    tmp_data = {}

    k = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '10']
    for name in data:
        tmp_data[name] = {}
        for i in k:
            acceleration_data = []

            for j in range(10):
                element = data[name]['0']
                elements = data[name][i]              
                tmp = 1 / (elements[j] /  element[j])

                acceleration_data.append(tmp)
            tmp_data[name][i] = acceleration_data

    for i in tmp_data:
        for j in k:
            y = tmp_data[i][j]
            x = arr
            
            plt.plot(x, y, label=f'parall {j}')

    plt.xlabel("size")
    plt.ylabel("Acceleration: 1 / (V(p) / V(1))")
    plt.legend(loc='upper left')
    plt.savefig(f'./assets/res_accel_Threads{arr[len(arr) - 1]}.png')
    plt.clf        



def graph_time_exec(arr, data):
    k = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '10']
    for i in data:
        for j in k:
            timing = data[i][j]
            size = arr

            plt.plot(size, timing, label=f'{i} {j}')

    plt.xlabel("size")
    plt.ylabel("time")
    plt.legend(loc='upper left')
    plt.savefig(f'./assets/res_time_Threads{arr[len(arr) - 1]}.png')
    plt.clf


def earn_data(arr):
    data = {}
    try:
        target = TargetDir.CLANG
        print(target)
        data[target.name] =  {}
        data[target.name]['0'] = run(target, '0', arr)
        data[target.name]['1'] = run(target, '1', arr)
        data[target.name]['2'] = run(target, '2', arr)
        data[target.name]['3'] = run(target, '3', arr)
        data[target.name]['4'] = run(target, '4', arr)
        data[target.name]['5'] = run(target, '5', arr)
        data[target.name]['6'] = run(target, '6', arr)
        data[target.name]['7'] = run(target, '7', arr)
        data[target.name]['8'] = run(target, '8', arr)
        data[target.name]['10'] = run(target, '10', arr)
    except KeyboardInterrupt:
        pass

    return data


def main():
   arr = n_variation()
   print("Arr is:", arr)
   data = earn_data(arr)
   graph_parallel(arr, data)
   #graph_time_exec(arr, data)


if __name__ == '__main__':
    main()