import os
import shutil
from enum import Enum

# Creating dir for files
class TargetDir(str, Enum):
    GCC = 'gcc-compiler'
    TCC = 'tcc-compiler'
    CLANG = 'clang-compiler'

# Classification of programs
class LabPrefix(str, Enum):
    NO_PARALLEL = 'lab1-no-parallel'
    PARALLEL = 'lab1-parallel'


def clear():
    for v in TargetDir:
        try:
            shutil.rmtree(f'./{v.value}')
        except FileNotFoundError:
            pass
        os.mkdir(v.value)

# Build for non parallel
def build_non_parallel() -> None:
    os.system(f'gcc -O3 -Wall -Werror -o {TargetDir.GCC}/{LabPrefix.NO_PARALLEL} lab1.c -lm')
    os.system(f'clang -O3 -fno-vectorize -fno-slp-vectorize -Wall -Werror -o {TargetDir.CLANG}/{LabPrefix.NO_PARALLEL} lab1.c -lm')
    os.system(f'tcc -O3 -Wall -Werror -o {TargetDir.TCC}/{LabPrefix.NO_PARALLEL} lab1.c -lm')

#  Build for parallel
def build_parallel(n_threads: int) -> None:
    os.system(
        (
            "gcc -O3 -Wall -Werror -floop-parallelize-all "
            f"-ftree-parallelize-loops={n_threads} lab1.c "
            f"-o {TargetDir.GCC}/{LabPrefix.PARALLEL}-{n_threads} -lm"
        )
    )
    os.system(
        (
            f"clang -O3 -Wall -Werror -mllvm -force-vector-width={n_threads} "
            f"lab1.c -o {TargetDir.CLANG}/{LabPrefix.PARALLEL}-{n_threads} -lm"
        )
    )
    os.system(
        (
            f"tcc -O3 -Wall -Werror -floop-parallelize-all "
            f"-ftree-parallelize-loops={n_threads} "
            f"lab1.c -o {TargetDir.TCC}/{LabPrefix.PARALLEL}-{n_threads} -lm"
        )
    )


def main():
    clear()
    build_non_parallel()
    k = [1, 2, 4, 6]
    for n_threads in k:
        build_parallel(n_threads)


if __name__ == '__main__':
    main()













