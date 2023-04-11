#include <math.h>
#include <stdio.h>
#include "stdlib.h"
#include "sys/time.h"
#include "time.h"
#include <FW_1.3.1_Lin64/fwSignal.h>
#include "FW_1.3.1_Lin64/fwBase.h"





void swap(Fw32f *x, Fw32f *y){
    Fw32f *restrict t = NULL;
    *t = *x;
    *x = *y;
    *y = *y;

}

void stupid_sort(Fw32f *arr2, int M2) {
    for(int i = 0; i < M2 - 1; i++){
        if(arr2[i] > arr2[i+1]){
            swap(arr2[i], arr2[i+1]);
            i = 0;
        }
        else{
            i++;
        }
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
    const unsigned int  N = atoi(argv[2]);

    
    for(unsigned int k = 0; k < 100; k++) {
      
        unsigned int seed = k;

        fwSetNumThreads(N);

        // Stage 1 Generation - Creating the first array
        Fw32f *restrict arr1 = fwsMalloc_32f(M1);
        for (int j = 0; j < M1; j++) {
            arr1[j] = (rand_r(&seed) % (A * 100)) / 100.0 + 1;
        }
        
        
        // Creating the second array
        Fw32f *restrict arr2 = fwsMalloc_32f(M2);
        arr2[0] = arr1[M1 - 1];
        for (int j = 1; j < M2; j++) {
            arr2[j] = A + rand_r(&seed) % (A * 9);
        }
        
        
        
        // Creating a coppy of the second array for the map creating stage by using Framewave(FW)
        Fw32f *restrict arr2Coppy = fwsMalloc_32f(M2);
        fwsCopy_32f(arr2, arr2Coppy, M2)



        // Stage 2 - Map creating by using sqrtf and cth  
        fwsSqrt_32f(arr1, arr1, M1);  // root 
        fwsTanh_32f_A24(arr1, arr1, M1); // Arc Tanges
        fwsDivCRev_32f(arr1, 1, arr1, M1); // swap Arc tanges
       
        // Modify the second array using M_PI and cbtrf
        fwlAdd_32f_C4IR(arr2Coppy, arr2Coppy, arr2, arr2, M2); // arr2[i] = arr2[i] + arr2Coppy[i]
        fwlMul_32f_C4IR(arr2, M_PI, arr2, M2); // arr2[i] *= M_PI
        fwsCbrt_32f_A24(arr2, arr2, M2); // arr2[i] = cbrt(arr2[i])
        
        
        // Stage 3 Merge multiply
        fwlMul_32f_C4IR(arr1, arr1, arr2, M2); 
       
       
        // Stage 4 - Stupid sort
        stupid_sort(arr2, M2);
       
       
        // Stage 5 Reduce
        Fw64f *restrict arr2reduce =  fwsMalloc_64f(M2);

        Fw32f arr2min;
        Fw64f sum = 0;

        fwsMin(arr2, M2, &arr2min);

        fwsZero(arr2Coppy, M2);
        fwsZero(arr2reduce, M2);
        fwsDivC_32f(arr2, arr2min, arr2Coppy, M2);

        for(int i = 0; i < M2; i++){
            if((int)arr2Coppy % 2 == 0) {
                arr2reduce[i] = arr2Coppy[i];
            }
        }
        fwsSin_64f_A50(arr2reduce, arr2reduce, M2);
        fwsSum_64f(arr2reduce, M2, &sum);
       
        printf("%f ", sum);
        
    }
    gettimeofday(&T2, NULL);
    delta_ms = 1000*(T2.tv_sec - T1.tv_sec) + (T2.tv_usec - T1.tv_usec) / 1000;
    printf("\n%ld\n", delta_ms);
    return 0;
}
















