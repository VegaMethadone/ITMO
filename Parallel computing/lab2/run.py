import os
import json
from build import TargetDir, LabPrefix, LIBS_DIR

"""
def n_config(target, time):
    with open('assets/n_config.json') as assets:
        data = json.load(assets)
        return data[target][time]
"""


def  run(target: TargetDir, prefix: LabPrefix, core: str):
    with open('assets/divide.json') as assets:
        data = json.load(assets)
    elements = data['CLANG']['8']
    print(elements)
       
     # FIX  
    time_array = []
    for i in range(len(elements)):
        liba = 'LD_LIBRARY_PATH="$PWD/FW_1.3.1_Lin64/lib"'
        path = f'{liba} ./{TargetDir.CLANG}/{LabPrefix.DEFAULT} {elements[i]} {core}'
        print(path)
        result = os.popen(path).read()
        nums, exectime = result.split('\n')[:2]
        print("Exectime: ", exectime)
        
        time_array.append(int(exectime))
        print("Array: ", time_array)

    return time_array

## LD_LIBRARY_PATH="$PWD/FW_1.3.1_Lin64/lib" ./target-clang/lab-2 10000 6

def main():
    data = {}
    data[TargetDir.CLANG] = {}

    core_usage = []
    for i in range(1, 17):
        core_usage.append(str(i))

    print(core_usage)

    try:
        for i in core_usage:
            data[TargetDir.CLANG][i] = run(TargetDir.CLANG, LabPrefix.DEFAULT, i)
            print("DATA IS:", data[TargetDir.CLANG][i])
    except KeyboardInterrupt:
        pass


    with open('./assets/parallel_time.json', 'w') as f:
        json.dump(data, f, indent=2)

        


if __name__ == '__main__':
    main()
