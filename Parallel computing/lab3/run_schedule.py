import os
import json
from enum import Enum


class TargetDir(str, Enum):
    dynamic = 'target-clang-scheduale-dynamic'
    guided = 'target-clang-scheduale-guided'
    static = 'target-clang-scheduale-static'

class LabPrefix(str, Enum):
    DEFAULT = 'lab-3'

def earn_data(target: TargetDir, cores: str):
    with open('assets/divide.json') as assets:
        data = json.load(assets) 
    
    elements = data['CLANG']['0']
    print(elements)

    res = []

    for i in range(10):
        lab_name = LabPrefix.DEFAULT
        options = f'OMP_NUM_THREADS={cores} OMP_DYNAMIC=FALSE '
        #OMP_DYNAMIC=FALSE
        result = os.popen(f'{options}./{target.value}/{lab_name} {elements[i]} {cores}').read()
        _, timing = result.split("\n")[:2]

        res.append(int(timing))
        print(res)

    return res


def main():
    data = {}

    try:
        for target in TargetDir:
            print(target)
            data[target.name] = {}
            data[target.name]['1'] = earn_data(target, '1')
            data[target.name]['4'] = earn_data(target, '4')
            data[target.name]['8'] = earn_data(target, '8')
            data[target.name]['10'] = earn_data(target, '10')
    except KeyboardInterrupt:
        pass

    with open('./assets/schedule.json', 'w') as f:
        json.dump(data, f, indent=2)

if __name__ == '__main__':
    main()