import os
import shutil
from enum import Enum

# Заменить в parallel_time.json target-clang на CLANG

class TargetDir(str, Enum):
    CLANG = 'target-clang-scheduale-dynamic'


class LabPrefix(str, Enum):
    DEFAULT = 'lab-3'


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
                f'{target.name.lower()} -O3 -Wall -Werror -fopenmp lab3dynamic.c '
                f'-o {target.value}/{LabPrefix.DEFAULT} -lm -lgomp'
            )
        )


def main():
    clear()
    build()


if __name__ == '__main__':
    main()