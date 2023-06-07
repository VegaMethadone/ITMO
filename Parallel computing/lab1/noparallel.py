import os
import json
from build import TargetDir, LabPrefix


def bin_search(array, key, l, r, target: TargetDir, prefix: LabPrefix):
    print("work")
    while l < r - 1:
        mid = (l + r) // 2
        result = os.popen(f'{target.value}/{prefix.value} {array[mid]}').read()
        nums, exectime = result.split('\n')[:2]
        print(exectime)
        if int(exectime) < key:
            l = mid
        else:
            r = mid
    
    return r


def main():
    arr = []
    for i in range(1000000):
        tmp = i
        arr.append(tmp)
    
    result = {}

    try:
        for target in TargetDir:
            print(target)
            for prefix in LabPrefix:
                if prefix == LabPrefix.NO_PARALLEL:
                    print(prefix)
                    result[target.name] = {}
                    result[target.name]['1000'] = bin_search(arr, 1000, -1, len(arr)-1, target, prefix)
                    result[target.name]['5000'] = bin_search(arr, 5000, -1, len(arr)-1, target, prefix)
    except KeyboardInterrupt:
        pass

    try:
        os.mkdir('assets')
    except FileExistsError:
        pass

    with open('./assets/n_config.json', 'w') as f:
        json.dump(result, f, indent=2)


if __name__ == '__main__':
    main()