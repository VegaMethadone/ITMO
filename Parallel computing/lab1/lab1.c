#include <math.h>
#include <stdio.h>
#include "stdlib.h"
#include "sys/time.h"
#include "time.h"


int main() {
    int M1, M2, N;
    float A;

    struct timeval T1, T2;
    long delta_ms;

    N = 10000;

    gettimeofday(&T1, NULL);
    for(unsigned int k = 0; k < 100; k++) {

        unsigned int seed = k;

        M1 = N;
        A = 100.00;
        M2 = M1 / 2;
        A *= 10-1;

        // Stage 1 Generation - Creating the first array
        float *restrict arr1 = malloc(M1 * sizeof(float));
        arr1[0] = 1.00;
        for (int j = 1; j < M1; j++) {
            int rand_num = rand_r(&seed);
            float rand_float = (float) rand_num / RAND_MAX;
            arr1[j] = (rand_float * A * 100) / 100;
        }


        // Creating the second array
        float *restrict arr2 = malloc(M2 * sizeof(float));
        arr2[0] = arr1[M1 - 1];
        for (int j = 1; j < M2; j++) {
            int rand_num = rand_r(&seed);
            float rand_float = (float) rand_num / RAND_MAX;
            arr2[j] = (rand_float * 9 * A + A) * 100 / 100;
        }


        // Creating a coppy of the second array for the map creating stage
        float *restrict arr2Coppy = malloc(M2  * sizeof(float));
        for(int i = 0; i < M2; i++){
            arr2Coppy[i] = arr2[i];
        }

        // Stage 2 - Map creating by using sqrtf and cth
        for(int i = 0; i < M1; i++){
            float tmp = arr1[i];
            tmp = sqrtf(tmp);
            arr1[i] = coshf(tmp) / sinhf(tmp);
        }


        // Modify the second array using M_PI and cbtrf
        for(int i = 1; i < M2; i++){
            float tmp = arr2[i] + arr2Coppy[i-1];
            tmp *= M_PI;
            arr2[i] = cbrtf(tmp);
        }
        arr2[0] = cbrtf(arr2[0]*M_PI);


        // Stage 3 Merge multiply
        for(int i = 0; i < M2; i++){
            float tmp = arr1[i] * arr2[i];
            arr2[i] = tmp;
        }


        // Stage 4 - Stupid sort
        for(int i = 0; i < M2-1; i++){
            if(arr2[i] > arr2[i+1]){
                float tmp = arr2[i];
                arr2[i] = arr2[i + 1];
                arr2[i + 1] = tmp;
                if(i != 0){
                    i -= 2;
                }
            }
        }



        // Stage 5 Reduce
        float sum = 0;
        float min = arr2[0];
        for(int i = 0; i < M2; i++){
            int tmp = (int)arr2[i] / (int)min;
            if(tmp % 2 == 0){
                sum += sinf(arr2[i]);
            }
        }
        printf("\n%f", sum);

    }
    gettimeofday(&T2, NULL);
    delta_ms = 1000*(T2.tv_sec - T1.tv_sec) + (T2.tv_usec - T1.tv_usec) / 1000;
    printf("\nN=%d. Milliseconds passed: %ld\n", N, delta_ms);
    return 0;
}