import os
import json
from build import TargetDir, LabPrefix


# Зайти в lab4.c и заменить в основном цикле программы размерность со 100 до 10


def n_variation():
    with open('./assets/n_config.json') as asset:
        data = json.load(asset)
        N1 = data['CLANG']['1000']
        N2 = data['CLANG']['5000']
        N = N2 - N1
        N //= 10
    res = [N1 + N * i for i in range(10)]
    return res

def run(target: TargetDir, cores: str, data):
    lab_name = LabPrefix.DEFAULT
    options = f'OMP_NUM_THREADS={cores} OMP_DYNAMIC=FALSE '
    res = []
    for i in range(10):
        new_res = []
        for j in range(10):
            print(f'{options}./{target.value}/{lab_name} {data[i]} {cores}')
            result = os.popen(f'{options}./{target.value}/{lab_name} {data[i]} {cores}').read()
            if cores == '0':
                _, timing = result.split("\n")[:2]
            else:
                timing = result.split("\n")
                print(timing)
                timing, _ = timing[len(timing) - 2:]
                new_res.append(int(timing))
        res.append(new_res)
        print(res)
    return res


def earn_data(arr):
    data = {}
    try:
        target = TargetDir.CLANG
        print(target)
        data[target.name] =  {}
        data[target.name]['2'] = run(target, '2', arr)
    except KeyboardInterrupt:
        pass

    return data


def main():
   arr = n_variation()
   print("Arr is:", arr)
   data = earn_data(arr)

   with open('./assets/doverirelni_interval.json', 'w') as f:
       json.dump(data, f, indent=2)
   


if __name__ == '__main__':
    main()
