import json
import os
import shutil
from build import TargetDir, LabPrefix
import matplotlib.pyplot as plt

def n_variation():
    with open('assets/divide.json') as assets:
        data = json.load(assets)
        N = data['CLANG']['0']
        N1 = N[0]
        N1 //= 10
        print(N1)
        res = [N1 + N1 * i for i in range(10)]

        return res
    

def n_variation_own(N):
    N1 = N // 10
    res = [N1 + N1 * i for i in range(10)]
    
    return res
    

def run(target, cores: str, data, optimisation:str):
    lab_name = f'lab-3-{optimisation}'
    options = ''
    if cores == '0':
        lab_name = f'lab-3-no-parallel-{optimisation}'
    else:
        options = f'OMP_NUM_THREADS={cores} OMP_DYNAMIC=FALSE '
    res = []
    for i in range(10):
        print(f'{options}./{target}/{lab_name} {data[i]} {cores}')
        result = os.popen(f'{options}./{target}/{lab_name} {data[i]} {cores}').read()
        _, timing = result.split("\n")[:2]
        res.append(int(timing))
    return res



def graph_parallel(arr, data, optimisation: str):
    
    tmp_data = {}

    k = ['0', '1', '2', '4', '6']
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
    plt.savefig(f'./assets/res_accel_{optimisation}.png')
    plt.clf        



def graph_time_exec(arr, data, optimisation: str):
    k = ['0', '1', '2', '4', '6']
    for i in data:
        for j in k:
            timing = data[i][j]
            size = arr

            plt.plot(size, timing, label=f'parall {j}')

    plt.xlabel("size")
    plt.ylabel("time")
    plt.legend(loc='upper left')
    plt.savefig(f'./assets/res_time_{optimisation}.png')
    plt.clf


def earn_data(arr, optimisation:str):
    data = {}
    try:
        target = 'optimisation_build'
        print(target)
        data[target] =  {}
        data[target]['0'] = run(target, '0', arr, optimisation)
        data[target]['1'] = run(target, '1', arr, optimisation)
        data[target]['2'] = run(target, '2', arr, optimisation)
        data[target]['4'] = run(target, '4', arr, optimisation)
        data[target]['6'] = run(target, '6', arr, optimisation)
    except KeyboardInterrupt:
        pass

    return data



def optimisation_build() -> None:
    for target in TargetDir:
        os.system(
            (
                f'{target.name.lower()} -O1 -Wall -Werror lab3.c '
                f'-o optimisation_build/{LabPrefix.NO_PARALLEL}-01 -lm -lgomp'
            )
        )
        os.system(
            (
                f'{target.name.lower()} -O1 -Wall -Werror -fopenmp lab3.c '
                f'-o optimisation_build/{LabPrefix.DEFAULT}-01 -lm -lgomp'
            )
        )
        os.system(
            (
                f'{target.name.lower()} -O2 -Wall -Werror lab3.c '
                f'-o optimisation_build/{LabPrefix.NO_PARALLEL}-02 -lm -lgomp'
            )
        )
        os.system(
            (
                f'{target.name.lower()} -O2 -Wall -Werror -fopenmp lab3.c '
                f'-o optimisation_build/{LabPrefix.DEFAULT}-02 -lm -lgomp'
            )
        )
        os.system(
            (
                f'{target.name.lower()} -O3 -Wall -Werror lab3.c '
                f'-o optimisation_build/{LabPrefix.NO_PARALLEL}-03 -lm -lgomp'
            )
        )
        os.system(
            (
                f'{target.name.lower()} -O3 -Wall -Werror -fopenmp lab3.c '
                f'-o optimisation_build/{LabPrefix.DEFAULT}-03 -lm -lgomp'
            )
        )

def clear():
        try:
            shutil.rmtree(f'./optimisation_build')
        except FileNotFoundError:
            pass
        os.mkdir(f'optimisation_build')

def main():
    #clear()
    #optimisation_build()
    arr = n_variation_own(806565)
    i = '01'
    data = earn_data(arr, i)
    graph_parallel(arr, data, i)
    #graph_time_exec(arr, data, i)



if __name__ == '__main__':
    main()