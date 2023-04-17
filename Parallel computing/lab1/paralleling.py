import os
import json
from build import TargetDir, LabPrefix



def calculate_n(target: TargetDir):
    with open(f'./assets/n_config.json') as assets:
        data = json.load(assets)
    N1 = data[f'{target.name}']['1000']
    N2 = data[f'{target.name}']['5000']
    N = (N2 - N1) // 10

    reulst = [N1 + N * i for i in range(1,11)]

    return reulst


def main():
    n_variants = {}
    try:
        for target in TargetDir:
            for prefix in LabPrefix.PARALLEL:        
                    n_variants[target.name] = {}
                    n_variants[target.name]['0'] = calculate_n(target)
                    n_variants[target.name]['1'] = calculate_n(target)
                    n_variants[target.name]['4'] = calculate_n(target)
                    n_variants[target.name]['6'] = calculate_n(target)
                    n_variants[target.name]['8'] = calculate_n(target)
    except KeyboardInterrupt:
        pass



    with open('./assets/divide.json', 'w') as f:
        json.dump(n_variants, f, indent=2)


        

if __name__ == '__main__':
    main()