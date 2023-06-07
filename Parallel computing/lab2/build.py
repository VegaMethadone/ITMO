import os
import shutil
from enum import Enum


class TargetDir(str, Enum):
    CLANG = 'target-clang'

class LabPrefix(str, Enum):
    DEFAULT = 'lab-2'


LIBS_DIR = 'FW_1.3.1_Lin64'


def clear():
    for target in TargetDir:
        try:
            shutil.rmtree(f'./{target.value}')
        except FileNotFoundError:
            pass
        os.mkdir(target.value)

def build() -> None:
    os.system(
        (
        f'clang -m64 -L{LIBS_DIR}/lib -Wall -Werror '
        f'-o {TargetDir.CLANG}/{LabPrefix.DEFAULT} lab2.c '
        '-lm -lfwSignal -lfwBase'
        )
    )

def main():
    clear()
    build()

if __name__ == '__main__':
    main()