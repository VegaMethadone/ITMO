import os 
import json
from build import TargetDir, LabPrefix


def elem_earning(target: TargetDir, k: str):
    with open('assets/divide.json') as assets:
        data = json.load(assets)
    elements = data[target.name][k]
    print('Elemets: ', elements)
        
    time_array = []
    for i in range(len(elements)):
            
        if k == '0':
            name = LabPrefix.NO_PARALLEL
        else:
            name = f'{LabPrefix.PARALLEL}-{k}'

        path = f'{target.value}/{name} {elements[i]}'
        print(path)
        
        result = os.popen(path).read()
        nums, exectime = result.split('\n')[:2]
        
        print("Exectime: ", exectime)
        
        time_array.append(int(exectime))
        print("Array: ", time_array)

    return time_array

def main():
    result = {}
    try:
        for target in TargetDir:
            print("Target: ", target)
            result[target.name] = {}
            result[target.name]['0'] = elem_earning(target, '0')
            result[target.name]['1'] = elem_earning(target, '1')
            result[target.name]['4'] = elem_earning(target, '4')
            result[target.name]['6'] = elem_earning(target, '6')
            result[target.name]['8'] = elem_earning(target, '8')
    except KeyboardInterrupt:
        pass

    try:
        os.mkdir('assets')
    except FileExistsError:
        pass

    with open('./assets/time_data.json', 'w') as f:
        json.dump(result, f, indent=2)


if __name__ == '__main__':
    main()
