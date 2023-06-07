import json
from build import TargetDir, LabPrefix
import matplotlib.pyplot as plt



def plt_save(target: TargetDir):
    with open('assets/divide.json') as divide:
        x = json.load(divide)
    
    with open('assets/time_data.json') as time_data:
        y = json.load(time_data)

    k = ['0', '1', '2', '4', '6']

    for i in k:
        size = x[target.name][i]
        ms   = y[target.name][i]
        plt.plot(size, ms, label=f"parallel {i}")

    plt.xlabel("Size of array")
    plt.ylabel("Exec ms")
    plt.legend()
    plt.savefig(f'./assets/{target.name}_results.png')
    plt.clf()

def main():
    try:
        for target in TargetDir:
            plt_save(target)
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
