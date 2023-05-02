import json
import os
from run_schedule import TargetDir, LabPrefix
import matplotlib.pyplot as plt


def graph(target):
    with open('assets/divide.json') as divid:
        divide = json.load(divid)
    
    with open('assets/schedule.json') as sch:
        schedule = json.load(sch)

    data = {}
    data[target.name] = {}
    k = ['1', '4', '8', '10']
    for i in k:
          data[target.name][i] = schedule[target.name][i]
        
    for j in k:
            timing = data[target.name][j]
            size = divide['CLANG']['0']
                
            plt.plot(size, timing, label=f'chunk-{j}')

    plt.title(target.name)
    plt.xlabel("size")
    plt.ylabel("timing")
    plt.legend(loc='upper left')
    plt.savefig(f'./assets/schedule-{target.name}.png')
    plt.clf

    data.clear()
    
def main():
   graph(TargetDir.static)

if __name__ == '__main__':
    main()
    


 
    