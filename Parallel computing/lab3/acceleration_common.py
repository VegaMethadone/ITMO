import matplotlib.pyplot as plt
import os
import json
from build import TargetDir, LabPrefix
from acceleration_json_maker import Accelertion

def graph(target: TargetDir):
    with open('assets/acceleration_time.json') as accel:
        acceleration_time = json.load(accel)
    with open('assets/parallel_time.json') as parall:
        parallel_time = json.load(parall)
    with open('assets/time_data.json') as time_da:
        time_data = json.load(time_da)
    with open('assets/divide.json') as div:
        divide = json.load(div)

    data = {}
    data['lab1'] = {} 
    data['lab2'] = {}
    data['lab3'] = {}

    k = ['1', '2', '4', '6']

    for i in k:
        data['lab1'][i] = time_data[target.name][i] 
        data['lab2'][i] = parallel_time[target.name][i]
        data['lab3'][i] = acceleration_time[target.name][i]
        
    for i in data:
        for j in k:
            timing = data[i][j]
            size = divide[target.name][j]
            
            plt.plot(size, timing, label=f'{i} {j}')

    plt.xlabel("Acceleration")
    plt.ylabel("Size")
    plt.legend(loc='upper left')
    plt.savefig('./assets/res_acceleration.png')
    plt.clf

    with open('./assets/labs_data.json', 'w') as f:
        json.dump(data, f, indent=2)


def main():
    graph(TargetDir.CLANG)

if __name__ == '__main__':
    main()