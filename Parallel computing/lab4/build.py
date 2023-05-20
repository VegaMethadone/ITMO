import os
import shutil
from enum import Enum

#  В папку assets добавить json file  из лабы lab1sort с данными N1 - N2 (n_config.json)
#   "CLANG": {
#    "1000": 1084,
#    "5000": 1877
#  }



class TargetDir(str, Enum):
    CLANG = 'target-clang'


class LabPrefix(str, Enum):
    DEFAULT = 'lab-4'
    NO_PARALLEL = 'lab-4-no-parallel'
    N_THREADS = 'lab-4-n-threads'


def clear():
    for v in TargetDir:
        try:
            shutil.rmtree(f'./{v.value}')
        except FileNotFoundError:
            pass
        os.mkdir(v.value)


def build() -> None:
    for target in TargetDir:
        os.system(
            (
                f'{target.name.lower()} -O3 -Wall -Werror  lab4.c '
                f'-o {target.value}/{LabPrefix.NO_PARALLEL} -lm -lgomp'
            )
        )
        os.system(
            (
                f'{target.name.lower()} -O3 -Wall -Werror -fopenmp lab4.c '
                f'-o {target.value}/{LabPrefix.DEFAULT} -lm -lgomp'
            )
        )
        os.system(
            (
                f'{target.name.lower()} -O3 -Wall -Werror -fopenmp lab4-nThreads.c '
                f'-o {target.value}/{LabPrefix.N_THREADS} -lm -lgomp'
            )
        )


def main():
    clear()
    build()


if __name__ == '__main__':
    main()