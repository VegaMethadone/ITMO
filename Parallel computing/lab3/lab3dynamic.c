#include <math.h>
#include <stdio.h>
#include "stdlib.h"
#include "sys/time.h"
#include "time.h"
#include "omp.h"

void swap(double *x, double *y ){
    double tmp;
    tmp = *x;
    *x = *y;
    *y = tmp;
}

//stupid_sort section
void stupid_sort(double *array,  int n) {
    int i = 0;
    while (i < n - 1) {
        if (array[i + 1] < array[i]) swap(array + i, array + i + 1), i = 0;
        else i++;
    }
}


int main(int argc, char *argv[]) {
    unsigned int M1, M2;
    int A;

    struct timeval T1, T2;
    long delta_ms;

    gettimeofday(&T1, NULL);

    M1 = atoi(argv[1]);
    M2 = M1 / 2;
    A = 100;

    

    double *restrict arr1 = malloc(M1 * sizeof(double));
    double *restrict arr2 = malloc(M2 * sizeof(double));
    double *restrict arr2Coppy = malloc(M2  * sizeof(double));

    #ifdef _OPENMP
        const unsigned int N = atoi(argv[2]);
        omp_set_schedule(omp_sched_dynamic, N);
        omp_set_dynamic(0);
        omp_set_num_threads(N);
    #endif

    for(unsigned int k = 0; k < 100; k++) {
      
        double sum = 0;
        unsigned int seed = k;


        // Stage 1 Generation - Creating the first array        
        for (int j = 0; j < M1; j++) {
            arr1[j] = (rand_r(&seed) % (A * 100)) / 100.0 + 1;
        }
        

        // Creating the second array        
        arr2[0] = arr1[M1 - 1];
        for (int j = 1; j < M2; j++) {
            arr2[j] = A + rand_r(&seed) % (A * 9);
        }

        #pragma omp parallel for default(none) shared(M2, arr2, arr2Coppy, A, seed) schedule(dynamic, N) firstprivate(N)
        {
            // Creating a coppy of the second array for the map creating stage       
            for(int i = 0; i < M2; i++){
                arr2Coppy[i] = arr2[i];
            }
        }

        #pragma omp parallel for default(none) shared(M1, arr1, A, seed) schedule(dynamic, N) firstprivate(N)
        {

            // Stage 2 - Map creating by using sqrtf and cth
            for(int i = 0; i < M1; i++){
                arr1[i] = cosh(sqrt(arr1[i])) / sinh(sqrt(arr1[i]));
            }
        }
        
        #pragma omp parallel for default(none) shared(M2, arr2, arr2Coppy, A, seed) schedule(dynamic, N) firstprivate(N)
        {
            // Modify the second array using M_PI and cbtrf
            for(int i = 1; i < M2; i++){
                arr2[i] = cbrt((arr2[i] + arr2Coppy[i-1]) * M_PI);
            }
        }
            arr2[0] = cbrt(arr2[0]*M_PI);
            
        #pragma omp parallel for default(none) shared(M2, arr1, arr2, A, seed) schedule(dynamic, N) firstprivate(N)
        {   
            // Stage 3 Merge multiply
            for(int i = 0; i < M2; i++){
                arr2[i] = arr1[i] * arr2[i];
            }
        }
            // Stage 4 - Stupid sort
            //stupid_sort(arr2, M2);
        
            // Stage 5 Reduce
        
        double min = arr2[0];
        #pragma omp parallel for default(none) shared(M2, arr2, min, A, seed) reduction(+:sum) schedule(dynamic, N) firstprivate(N)
            //#pragma omp parallel for reduction(+:sum)
        {
            for(int i = 0; i < M2; i++){
                if(((int)arr2[i] / (int)min) % 2 == 0){
                    sum += sin(arr2[i]);
                }
            }
        }

        printf("%f ", sum);
        
    }
    //omp_sched_t kind;
    //int chunk_size;
    //omp_get_schedule(&kind, &chunk_size);
    //printf("Schedule type: %d\n", kind);
    //printf("Chunk size: %d\n", chunk_size);
    gettimeofday(&T2, NULL);
    delta_ms = 1000*(T2.tv_sec - T1.tv_sec) + (T2.tv_usec - T1.tv_usec) / 1000;
    printf("\n%ld\n", delta_ms);
    return 0;
}
