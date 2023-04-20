#include <math.h>
#include <stdio.h>
#include "stdlib.h"
#include "sys/time.h"
#include "time.h"



void stupid_sort(double *arr2, int M2){
    for(int i = 0; i < M2-1; i++){
            if(arr2[i] > arr2[i+1]){
                double tmp = arr2[i];
                arr2[i] = arr2[i + 1];
                arr2[i + 1] = tmp;
                if(i != 0){
                    i -= 2;
                }
            }
        }
}


int main(int argc, char *argv[]) {
    unsigned int M1, M2;
    int A;

    struct timeval T1, T2;
    long delta_ms;

    gettimeofday(&T1, NULL);

    
    for(unsigned int k = 0; k < 100; k++) {
      
        unsigned int seed = k;

        M1 = atoi(argv[1]);
        M2 = M1 / 2;
        A = 100;

        // Stage 1 Generation - Creating the first array
        double *restrict arr1 = malloc(M1 * sizeof(double));
        for (int j = 0; j < M1; j++) {
            arr1[j] = (rand_r(&seed) % (A * 100)) / 100.0 + 1;
        }
        
        // Creating the second array
        double *restrict arr2 = malloc(M2 * sizeof(double));
        arr2[0] = arr1[M1 - 1];
        for (int j = 1; j < M2; j++) {
            arr2[j] = A + rand_r(&seed) % (A * 9);
        }
        
        // Creating a coppy of the second array for the map creating stage
        double *restrict arr2Coppy = malloc(M2  * sizeof(double));
        for(int i = 0; i < M2; i++){
            arr2Coppy[i] = arr2[i];
        }

        // Stage 2 - Map creating by using sqrtf and cth
        for(int i = 0; i < M1; i++){
            double tmp = arr1[i];
            tmp = sqrt(tmp);
            arr1[i] = cosh(tmp) / sinh(tmp);
        }       
       
        // Modify the second array using M_PI and cbtrf
        for(int i = 1; i < M2; i++){
            double tmp = arr2[i] + arr2Coppy[i-1];
            tmp *= M_PI;
            arr2[i] = cbrt(tmp);
        }
        arr2[0] = cbrt(arr2[0]*M_PI);             
        
        // Stage 3 Merge multiply
        for(int i = 0; i < M2; i++){
            double tmp = arr1[i] * arr2[i];
            arr2[i] = tmp;
        }
                   
        // Stage 4 - Stupid sort
        stupid_sort(arr2, M2);
            
        // Stage 5 Reduce
        double sum = 0;
        double min = arr2[0];
        for(int i = 0; i < M2; i++){
            int tmp = (int)arr2[i] / (int)min;
            if(tmp % 2 == 0){
                sum += sin(arr2[i]);
            }
        }
        printf("%f ", sum);
        
    }
    gettimeofday(&T2, NULL);
    delta_ms = 1000*(T2.tv_sec - T1.tv_sec) + (T2.tv_usec - T1.tv_usec) / 1000;
    printf("\n%ld\n", delta_ms);
    return 0;
}
