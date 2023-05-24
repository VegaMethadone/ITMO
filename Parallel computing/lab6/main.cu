#include <math.h>
#include <stdio.h>
#include "stdlib.h"
#include "time.h"
#include "string.h"
#include "cuda.h"
#include "cuda_runtime.h"
#include <curand.h>
#include <curand_kernel.h>
//#include "cuda_runtime_api.h"

#define M_PI           3.14159265358979323846
//#define DEBUG_MERGE
//#define DEBUG_REDUCE
//#define DEBUG



//print section
void print_arr(double *arr, int n){
    for(int i = 0; i < n; i++)
    {
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

//merge section
void merge(double *arr, int n){
    double *arr1 = (double*)malloc(n/2 * sizeof(double ));
    double *arr2 =(double *)malloc((n - n/2)* sizeof(double ));
                    //new double [n - n/2];

    for(int i = 0; i < n/2; i++){
        arr1[i] = arr[i];
    }

    #ifdef DEBUG_MERGE
        printf("Merge of sorted arr1 \n");
        print_arr(arr1, n/2);
    #endif

    int current = 0;
    for(int i = n/2; i < n; i++){
        arr2[current] = arr[i];
        current += 1;
    }

    #ifdef DEBUG_MERGE
    printf("Merge of sorted arr2 \n");
        print_arr(arr2, n - n/2);
    #endif

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
    free(arr1);
    free(arr2);
}


__global__ void randomKernel(unsigned int seed, double *array, int n, int A, int option){
    int tid = blockIdx.x * blockDim.x + threadIdx.x;
    curandState_t state;

    curand_init(seed, tid, 0, &state);
    // Generation for the first Array
    if(option == 1)
    {
        for (int i = tid; i < n; i += blockDim.x * gridDim.x)
        {
            unsigned int randomValue = curand(&state);
            array[i] = (randomValue % (A * 100)) / 100.0 + 1;
        }
    }
    // Generation for the second Array
    else
    {
        for (int i = tid; i < n; i += blockDim.x * gridDim.x)
        {
            unsigned int randomValue = curand(&state);
            array[i] = (A + randomValue % (A * 9));
        }
    }

}

__global__ void copyKernel(double *arr2, double *arr2Copy, int M2){
    int tid = blockIdx.x * blockDim.x + threadIdx.x;
    if(tid < M2)
    {
        arr2Copy[tid] = arr2[tid];
    }
}

__global__ void mapSqrtCthKernel(double *arr1, int M1){
    int tid = blockIdx.x * blockDim.x + threadIdx.x;
    if(tid < M1)
    {
        arr1[tid] = sqrt(cosh(arr1[tid] / sinh(arr1[tid])));
    }
}

__global__ void mapPiCbrtKernel(double *arr2, double *arr2Copy, int M2){
    int tid = blockIdx.x * blockDim.x + threadIdx.x;
    if(tid == 0)
    {
        arr2[tid] = cbrt(arr2[tid]*M_PI);
    }
    if(tid > 0 &&  tid < M2)
    {
        arr2[tid] = cbrt((arr2[tid] + arr2Copy[tid]) * M_PI);
    }
}

__global__ void multiplayKenrel(double *arr1, double *arr2, int M2){
    int tid = blockIdx.x * blockDim.x + threadIdx.x;
    if(tid < M2)
    {
        arr2[tid] = arr1[tid] * arr2[tid];
    }
}

__global__ void stupidSortKernel(double *array, int n) {
    int tid = threadIdx.x + blockIdx.x * blockDim.x;
    int half = n / 2;

    double *leftArray = array;
    double *rightArray = array + half;

    if (tid < half) {
        int i = 0;
        while (i < half - 1) {
            if (leftArray[i + 1] < leftArray[i]) {
                double temp = leftArray[i];
                leftArray[i] = leftArray[i + 1];
                leftArray[i + 1] = temp;
                i = 0;
            } else {
                i++;
            }
        }
    } else {
        int i = 0;
        while (i < n - half - 1) {
            if (rightArray[i + 1] < rightArray[i]) {
                double temp = rightArray[i];
                rightArray[i] = rightArray[i + 1];
                rightArray[i + 1] = temp;
                i = 0;
            } else {
                i++;
            }
        }
    }
    __syncthreads();

    if (tid < n - half) {
        array[tid] = leftArray[tid];
    } else {
        array[tid] = rightArray[tid - half];
    }
}
__constant__ double minValue;

__global__ void reduceKernel(double *arr2, int M2, float *blockSums){
    __shared__ float sum;
    sum = 0;

#ifdef DEBUG_REDUCE
    printf("Start sum is: %f\n", sum);
#endif

    int tid = threadIdx.x + blockIdx.x * blockDim.x;
    int stride = blockDim.x * gridDim.x;
#ifdef DEBUG_REDUCE
    printf("Tid is: %d\n", tid);
    printf("Stride is: %d\n", stride);
#endif

    if(tid < M2){
        if(((int)arr2[tid] / (int)arr2[0]) % 2 == 0)
        {
            atomicAdd(blockSums, (float)arr2[tid]);
        }
    }
}

//int argc, char *argv[]
int main() {
    #ifdef DEBUG
            printf("> Creating cuda events\n");
    #endif

    cudaError_t error = cudaGetLastError();
    cudaEvent_t start, end;
    cudaEventCreate(&start);
    cudaEventCreate(&end);

    #ifdef DEBUG
        printf("- Events are created\n");
    #endif

    int k = 0;

    int M1, M2;
    int A;
    //M1 = atoi(argv[1]);
    M1 = 1000;
    M2 = M1 / 2;
    A = 100;


    double *arr1;
    double *arr2;
    double *arr2Copy;

    #ifdef DEBUG
        printf("> Allocate memory for arrays\n");
    #endif

    cudaMalloc((void**)&arr1, M1 * sizeof (double ));
    cudaMalloc((void**)&arr2, M2 * sizeof(double ));
    cudaMalloc((void**)&arr2Copy, M2 * sizeof(double));
    if (error != cudaSuccess) {
        printf("CUDA error: %s\n", cudaGetErrorString(error));
    }
    double *arr1_host = (double*)malloc(M1 * sizeof(double));
    double *arr2_host = (double*)malloc(M2 * sizeof(double));
    double *arr2Copy_host = (double*)malloc(M2 * sizeof(double ));;

    #ifdef DEBUG
        double *arr1_host = (double*)malloc(M1 * sizeof(double));
        double *arr2_host = (double*)malloc(M2 * sizeof(double));
        double *arr2Copy_host = (double*)malloc(M2 * sizeof(double ));;
    #endif

    #ifdef DEBUG
        printf("- Memory are allocated\n");
    #endif


    cudaEventRecord(start);
    if (error != cudaSuccess) {
        printf("CUDA error: %s\n", cudaGetErrorString(error));
    }
    for(k = 0; k < 100; k++) {
        unsigned int seed = k;

        // Arrays generation
        #ifdef DEBUG
                printf("> Initialization of threads block for generator\n");
        #endif

        int threadsPerBlock = 1024;
        int blocksPerGridArr1 = (M1 + threadsPerBlock - 1) / threadsPerBlock;
        int blocksPerGridArr2 = (M2 + threadsPerBlock - 1) / threadsPerBlock;
        #ifdef DEBUG
                printf("> Start of generator\n");
        #endif

        // Creating arrays
        randomKernel<<<blocksPerGridArr1, threadsPerBlock>>>(seed, arr1, M1, A, 1);
        randomKernel<<<blocksPerGridArr2, threadsPerBlock>>>(seed, arr2, M2, A, 2);
        copyKernel<<<blocksPerGridArr2, threadsPerBlock>>>(arr2, arr2Copy, M2);

        #ifdef DEBUG
                printf("- Generation is succeed\n");
                printf("> Closing cores\n");
        #endif
        cudaDeviceSynchronize();

        #ifdef  DEBUG
            cudaMemcpy(arr1_host, arr1, M1 * sizeof(double), cudaMemcpyDeviceToHost);
            cudaMemcpy(arr2_host, arr2, M2 * sizeof(double), cudaMemcpyDeviceToHost);
            print_arr(arr1_host, M1);
            print_arr(arr2_host, M2);
        #endif

        // Stage 2 - Map creating
        #ifdef DEBUG
            printf("> Stage 2 - Map creating  \n");
        #endif
        mapSqrtCthKernel<<<blocksPerGridArr2, threadsPerBlock>>>(arr1, M1);
        mapPiCbrtKernel<<<blocksPerGridArr2, threadsPerBlock>>>(arr2, arr2Copy, M2);
        #ifdef DEBUG
                printf("- Stage 2 - Map is done !\n");
        #endif
        cudaDeviceSynchronize();
        #ifdef DEBUG
                printf("> arr2[0] = cbrt(arr2[0]*M_PI); \n");
        #endif
        //arr2[0] = cbrt(arr2[0]*M_PI);

        #ifdef  DEBUG
            cudaMemcpy(arr1_host, arr1, M1 * sizeof(double), cudaMemcpyDeviceToHost);
            cudaMemcpy(arr2_host, arr2, M2 * sizeof(double), cudaMemcpyDeviceToHost);
            print_arr(arr1_host, M1);
            print_arr(arr2_host, M2);
        #endif
        // Stage  3 - Merge multiply
        #ifdef DEBUG
                printf("> Stage 3 - Merge \n");
        #endif
        multiplayKenrel<<<blocksPerGridArr2, threadsPerBlock>>>(arr1, arr2, M2);
        #ifdef DEBUG
                printf("> Stage 3 - Merge is done ! \n");
        #endif
        cudaDeviceSynchronize();

        #ifdef  DEBUG
            cudaMemcpy(arr2_host, arr2, M2 * sizeof(double), cudaMemcpyDeviceToHost);
            print_arr(arr2_host, M2);
        #endif

        // Stage 4 - sort
        #ifdef DEBUG
                printf("> Stage 4 - Sort \n");
        #endif
        stupidSortKernel<<<blocksPerGridArr2, threadsPerBlock>>>(arr2, M2);
        cudaDeviceSynchronize();
        #ifdef DEBUG
                printf("- Stage 4 - Sort is done\n");
        #endif
        #ifdef  DEBUG
                cudaMemcpy(arr2_host, arr2, M2 * sizeof(double), cudaMemcpyDeviceToHost);
                print_arr(arr2_host, M2);
        #endif
        cudaMemcpy(arr2_host, arr2, M2 * sizeof(double), cudaMemcpyDeviceToHost);
        #ifdef DEBUG
                printf("> Merge of sorted array\n");
        #endif
        merge(arr2_host, M2);
        #ifdef DEBUG
                printf("- Merge of sorted array is done\n");
                print_arr(arr2_host, M2);
        #endif
        cudaMemcpy(arr2, arr2_host, M2 * sizeof(double), cudaMemcpyHostToDevice);
        #ifdef DEBUG
                printf("- From host to device arr2copy\n");
        #endif
        // Stage 5 - Reduce
        float sum = 0.0f;
        float *deviceSum;
        cudaMalloc((void**)&deviceSum, sizeof(float));

        #ifdef DEBUG
                printf("> Stage 5 - Reduce \n");
        #endif

        cudaMemcpy(deviceSum, &sum, sizeof(float), cudaMemcpyHostToDevice);
        reduceKernel<<<blocksPerGridArr2, threadsPerBlock>>>(arr2, M2, deviceSum);
        cudaDeviceSynchronize();

        float hostResult;
        cudaMemcpy(&hostResult, deviceSum, sizeof(float), cudaMemcpyDeviceToHost);

        #ifdef DEBUG
                printf("- Stage 5 - Reduce is done\n");
        #endif

        cudaFree(deviceSum);
        printf("%f ", hostResult);

    }
    cudaEventRecord(end);
    cudaEventSynchronize(end);

    cudaFree(arr1);
    cudaFree(arr2);
    cudaFree(arr2Copy);
    free(arr1_host);
    free(arr2_host);
    free(arr2Copy_host);

    float milliseconds = 0;
    cudaEventElapsedTime(&milliseconds, start, end);
    printf("\nExecution time of GPU: %f ms\n", milliseconds);
    return 0;
}
