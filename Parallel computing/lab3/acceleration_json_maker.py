import matplotlib.pyplot as plt
import os
import json
from build import TargetDir, LabPrefix



def Accelertion(target: TargetDir):
    with open('assets/labs_data.json') as assets:
        json_data = json.load(assets)

    with open('assets/divide.json') as divid:
        divide = json.load(divid)
    

    data = {}
    k = ['1', '2', '4', '6']
    for name in json_data:
        print(name)
        data[name] = {}
        for i in k:
            print("Cores", i)
            accelertion_data = []

            for j in range(10):
                
                element = json_data[name]['1']
                elements = json_data[name][i]
                tmp = 1 / (elements[j] / element[j])
                    
                accelertion_data.append(tmp)
            data[name][i] = accelertion_data

        
    for i in data:
        for j in k:
            y = data[i][j]
            x = divide[target.name][j]
            
            plt.plot(x, y, label=f'{i} {j}')

    plt.xlabel("size")
    plt.ylabel("Acceleration: 1 / (V(p) / V(1))")
    plt.legend(loc='upper left')
    plt.savefig('./assets/acceleration_labs.png')
    plt.clf
    

def main():
    Accelertion(TargetDir.CLANG)

if __name__ == '__main__':
    main()
