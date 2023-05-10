#include <math.h>
#include <stdio.h>
#include "stdlib.h"
#include "sys/time.h"
#include "time.h"
#include "omp.h"
#include "string.h"
#include "unistd.h"


#ifdef _OPENMP
    #include "omp.h"
#else
    int omp_get_num_procs() {return 1;}
#endif


//print section
void print_arr(double *arr, int n){
    for(int i = 0; i < n; i++){
        printf("%f ", arr[i]);
    }
    printf("\n");
}

//swap section
void swap(double *x, double *y) {
    double tmp;
    tmp = *x;
    *x = *y;
    *y = tmp;
}

//stupid_sort section
void stupid_sort(double *array, int l, int r) {
    int i = l;
    while (i < r - 1) {
        if (array[i + 1] < array[i]) swap(array + i, array + i + 1), i = l;
        else i++;
    }
}

//merge section
void merge(double *arr, int n){
    double arr1 [n/2];
    double arr2 [n - n/2];

    for(int i = 0; i < n/2; i++){
        arr1[i] = arr[i];
    }
    //print_arr(arr1, n/2);
    int current = 0;
    for(int i = n/2; i < n; i++){
        arr2[current] = arr[i];
        current += 1;
    }
    //print_arr(arr2, n - n/2);

    int n1 = n/2;
    int n2= n - n/2;
    int l = 0;
    int r = 0;
    current = 0;

    while(l < n1 && r < n2){
        if(arr1[l] <= arr2[r]){
            arr[current] = arr1[l];
            l += 1;
        } else {
            arr[current] = arr2[r];
            r += 1;
        }
        current += 1;
    }

    while(l < n1){
        arr[current] = arr1[l];
        l += 1;
        current += 1;
    }

    while(r < n2) {
        arr[current] = arr2[r];
        r += 1;
        current += 1;
    }
    
}

//parallel sort section
void parallel_sort(double *arr, int n){
    
    #pragma omp parallel sections
    {
        #pragma omp section
        {
            stupid_sort(arr, 0, n/2);
        }
        #pragma omp section
        {
            stupid_sort(arr, n - n/2, n);
        }
    }

    merge(arr, n);

    //print_arr(arr, n);    
}


//main section
int main(int argc, char *argv[]) {
    unsigned int M1, M2;
    int A;
    int k = 0;
    int progress = 0;
    double start, end;

    start = omp_get_wtime();

    #pragma omp parallel sections num_threads(2) shared(k, progress)
    {
        #ifdef _OPENMP
            #pragma omp section
            {
                while(progress < 1){
                    double progress_time = omp_get_wtime();
                    printf("\nTime is: %f", (progress_time - start) * 1000.0);
                    printf("\nPROGRESS: %d\n", k);
                    usleep(1000000);
                }
            }
        #endif

        #pragma omp section
        {
            M1 = atoi(argv[1]);
            M2 = M1 / 2;
            A = 100;

            double *restrict arr1 = malloc(M1 * sizeof(double));
            double *restrict arr2 = malloc(M2 * sizeof(double));
            double *restrict arr2Coppy = malloc(M2  * sizeof(double));

            #ifdef _OPENMP
                const unsigned int N = atoi(argv[2]);
                //omp_set_schedule(omp_sched_auto, N);
                omp_set_dynamic(0);
                omp_set_num_threads(N);
            #endif

            for(k = 0; k < 100; k++) {
            
                double sum = 0;
                unsigned int seed = k;


                // Stage 1 Generation
                //Creating the first array        
                for (int j = 0; j < M1; j++) {
                    arr1[j] = (rand_r(&seed) % (A * 100)) / 100.0 + 1;
                }
                

                // Creating the second array        
                arr2[0] = arr1[M1 - 1];
                for (int j = 1; j < M2; j++) {
                    arr2[j] = A + rand_r(&seed) % (A * 9);
                }

                #pragma omp parallel for default(none) shared(M2, arr2, arr2Coppy, A, seed) 
                {
                    // Creating a coppy of the second array for the map creating stage       
                    for(int i = 0; i < M2; i++){
                        arr2Coppy[i] = arr2[i];
                    }
                }

                #pragma omp parallel for default(none) shared(M1, arr1, A, seed) 
                {

                    // Stage 2 - Map creating by using sqrtf and cth
                    for(int i = 0; i < M1; i++){
                        arr1[i] = cosh(sqrt(arr1[i])) / sinh(sqrt(arr1[i]));
                    }
                }
                
                #pragma omp parallel for default(none) shared(M2, arr2, arr2Coppy, A, seed) 
                {
                    // Modify the second array using M_PI and cbtrf
                    for(int i = 1; i < M2; i++){
                        arr2[i] = cbrt((arr2[i] + arr2Coppy[i-1]) * M_PI);
                    }
                }
                    arr2[0] = cbrt(arr2[0]*M_PI);
                    
                #pragma omp parallel for default(none) shared(M2, arr1, arr2, A, seed) 
                {   
                    // Stage 3 Merge multiply
                    for(int i = 0; i < M2; i++){
                        arr2[i] = arr1[i] * arr2[i];
                    }
                }
                    // Stage 4 - Stupid sort
                    parallel_sort(arr2, M2);
                
                    // Stage 5 Reduce
                
                double min = arr2[0];
                #pragma omp parallel for default(none) shared(M2, arr2, min, A, seed) reduction(+:sum) 
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

            progress = 1;

        }
    }
    end = omp_get_wtime();
    printf("%f\n", (end-start) * 1000.0);
    return 0;
}
















