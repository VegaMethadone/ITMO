#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

int main(){
    // clang -O3 -fopenmp schedule.c -o schedule
    #ifdef _OPENMP
        omp_set_dynamic(0);
        omp_set_num_threads(1);
    #endif

    int sum = 0;
    int nthreads, tid;
    #pragma omp parallel shared(sum) private(tid) default(none)
    {
        tid = omp_get_thread_num();
        #pragma omp for schedule(auto)
        for(int i = 0; i < 10000; i++){
            #pragma omp critical
            sum += i;
        }
    }
    printf("SUM = %d\n", sum);
    omp_sched_t kind;
    int chunk_size;
    omp_get_schedule(&kind, &chunk_size);
    printf("Schedule type: %d\n", kind);
    printf("Chunk size: %d\n", chunk_size);
    return 0;
}