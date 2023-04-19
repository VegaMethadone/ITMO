import json
from build import TargetDir, LabPrefix
import matplotlib.pyplot as plt 


def plt_save(target: TargetDir.CLANG):
    with open('assets/parallel_time.json') as parallel_time:
        y = json.load(parallel_time)
        
    with open('assets/divide.json') as divide:
        x = json.load(divide)

    core_usage = []
    for i in range(1, 17):
        core_usage.append(str(i))
    
    size = x['CLANG']['0']
    for i in core_usage:
        ms = y['target-clang'][i]
        plt.plot(size, ms, label=f'parallel {i}')

    plt.xlabel("Size of array")
    plt.ylabel("Exec ms")
    plt.legend(loc="center left")
    plt.savefig('./assets/clang_results.png')
    plt.clf()
       

def main():
    plt_save(TargetDir)
    #test()





if __name__ == '__main__':
    main()
