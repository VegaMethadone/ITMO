# S(p) = v(p) / v(1) , V(p) - average 
import json
import os
from build import TargetDir, LabPrefix



def earn_data(target: TargetDir, cores: str):
    with open('assets/divide.json') as assets:
        data = json.load(assets) 
    
    elements = data[target.name][cores]
    print(elements)

    res = []
    
    for i in range(10):
            
        lab_name = LabPrefix.DEFAULT
        options = ''

        if cores == '0':
            lab_name = LabPrefix.NO_PARALLEL
        else:
            options = f'OMP_NUM_THREADS={cores} OMP_DYNAMIC=FALSE '
    
        print(f'{options}./{target.value}/{lab_name} {elements[i]} {cores}')
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
            data[target.name]['0'] = earn_data(target, '0')
            data[target.name]['1'] = earn_data(target, '1')
            data[target.name]['2'] = earn_data(target, '2')
            data[target.name]['4'] = earn_data(target, '4')                    
            data[target.name]['6'] = earn_data(target, '6')
    except KeyboardInterrupt:
        pass

    try:
        os.mkdir('assets')
    except FileExistsError:
        pass

    with open('./assets/acceleration_time.json', 'w') as f:
        json.dump(data, f, indent=2)


if __name__ == '__main__':
    main()