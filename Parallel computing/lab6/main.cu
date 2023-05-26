#include <stdio.h>
#include <curand_kernel.h>

#define M_PI           3.14159265358979323846
//#define time_event
//#define DEBUG

//print section
void print_arr(double *arr, int n){
    for(int i = 0; i < n; i++)
    {
        printf("%f ", arr[i]);
    }
    printf("\n");
}
//blockIdx.x * blockDim.x + threadIdx.x
__global__ void randomKernel1(unsigned int seed, double *array, int n, int A){
    int tid = blockIdx.x * blockDim.x + threadIdx.x;
    curandState_t state;
    __shared__ double sharedArray[512];

    curand_init(seed, tid, 0, &state);

    if(tid < n){
        sharedArray[threadIdx.x] = array[tid];
    }
    __syncthreads();

    // Generation for the first Array

    if(tid < n){
        unsigned int randomValue = curand(&state);
        sharedArray[threadIdx.x] = (randomValue % (A * 100)) / 100.0 + 1;
        //array[i] = (randomValue % (A * 100)) / 100.0 + 1;

    }
    __syncthreads();

    if (tid < n) {
        array[tid] = sharedArray[threadIdx.x];
    }
}
__global__ void randomKernel2(unsigned int seed, double *array, int n, int A){
    int tid = blockIdx.x * blockDim.x + threadIdx.x;
    curandState_t state;
    __shared__ double sharedArray[512];

    curand_init(seed, tid, 0, &state);

    if(tid < n){
        sharedArray[threadIdx.x] = array[tid];
    }
    __syncthreads();

    if(tid < n){
        unsigned int randomValue = curand(&state);
        sharedArray[threadIdx.x] = A + randomValue % (A * 9);
        //array[i] = (A + randomValue % (A * 9));
    }

    __syncthreads();

    if (tid < n) {
        array[tid] = sharedArray[threadIdx.x];
    }
}
__global__ void copyKernel(double *arr2, double *arr2Copy, int M2){
    int tid =  blockIdx.x * blockDim.x + threadIdx.x;
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
    __syncthreads();
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


__global__ void reduceKernel(double *arr2, int M2, float *blockSums){

    int tid = blockIdx.x * blockDim.x + threadIdx.x;

    if(tid < M2){
        if(((int)arr2[tid] / (int)arr2[0]) % 2 == 0)
        {
            atomicAdd(blockSums, (float) sin(arr2[tid]));
        }
    }
}


int main(){
#ifdef DEBUG
    printf("> Creating cuda events\n");
#endif
    // Declaration of time events
    cudaError_t error = cudaGetLastError();
    cudaEvent_t start, end;
#ifdef time_event
    cudaEvent_t startGeneration, endGeneration;
    cudaEvent_t startStage2, endStage2;
    cudaEvent_t startStage3, endStage3;
    cudaEvent_t startStage5, endStage5;
#endif
    // Creating time events
    cudaEventCreate(&start);
    cudaEventCreate(&end);
#ifdef time_event
    cudaEventCreate(&startGeneration);
    cudaEventCreate(&endGeneration);
    cudaEventCreate(&startStage2);
    cudaEventCreate(&endStage2);
    cudaEventCreate(&startStage3);
    cudaEventCreate(&endStage3);
    cudaEventCreate(&startStage5);
    cudaEventCreate(&endStage5);
#endif
#ifdef DEBUG
    printf("- Events are created\n");
#endif

    float milliseconds;
    int k = 0;

    int M1, M2;
    int A;
    //M1 = atoi(argv[1]);
    M1 = 742107;
    M2 = M1 / 2;
    A = 100;

    double *arr1;
    double *arr2;
    double *arr2Copy;
    // Allocate memory on device
    cudaMalloc((void**)&arr1, M1 * sizeof (double ));
    cudaMalloc((void**)&arr2, M2 * sizeof(double ));
    cudaMalloc((void**)&arr2Copy, M2 * sizeof(double));
    if (error != cudaSuccess) {
        printf("CUDA error: %s\n", cudaGetErrorString(error));
    }

#ifdef DEBUG
    double *arr1_host = (double*)malloc(M1 * sizeof(double));
    double *arr2_host = (double*)malloc(M2 * sizeof(double));
    double *arr2Copy_host = (double*)malloc(M2 * sizeof(double ));
#endif
#ifdef DEBUG
    printf("- Memory are allocated\n");
#endif

    // Calculate of
    int threadsPerBlock = 512;
    int blocksPerGridArr1 = (M1 + threadsPerBlock - 1) / threadsPerBlock;
    int blocksPerGridArr2 = (M2 + threadsPerBlock - 1) / threadsPerBlock;

    cudaEventRecord(start);
    if (error != cudaSuccess) {
        printf("CUDA error: %s\n", cudaGetErrorString(error));
    }
    for(k = 0; k< 100; k++){
        unsigned int seed = k;

        // Creating arrays
#ifdef time_event
        cudaEventRecord(startGeneration);
#endif
#ifdef DEBUG
        printf("> Initialization of threads block for generator\n");
#endif
#ifdef DEBUG
        printf("> Start of generator\n");
#endif
        randomKernel1<<<blocksPerGridArr1, threadsPerBlock>>>(seed, arr1, M1, A);
        randomKernel2<<<blocksPerGridArr2, threadsPerBlock>>>(seed, arr2, M2, A);
        copyKernel<<<blocksPerGridArr2, threadsPerBlock>>>(arr2, arr2Copy, M2);
#ifdef DEBUG
        printf("- Generation is succeed\n");
                printf("> Closing cores\n");
#endif
#ifdef  DEBUG
        cudaMemcpy(arr1_host, arr1, M1 * sizeof(double), cudaMemcpyDeviceToHost);
        cudaMemcpy(arr2_host, arr2, M2 * sizeof(double), cudaMemcpyDeviceToHost);
        cudaMemcpy(arr2Copy_host, arr2Copy, M2 * sizeof(double), cudaMemcpyDeviceToHost);
        print_arr(arr1_host, M1);
        print_arr(arr2_host, M2);
        print_arr(arr2Copy_host, M2);
#endif
#ifdef time_event
        cudaEventRecord(endGeneration);
        cudaEventSynchronize(endGeneration);
        cudaEventElapsedTime(&milliseconds, startGeneration, endGeneration);
        printf("\nTime of stage 1: %f ms\n", milliseconds);
#endif
        // Stage 2 - Map creating
#ifdef time_event
        cudaEventRecord(startStage2);
#endif
#ifdef DEBUG
        printf("> Stage 2 - Map creating  \n");
#endif
        mapSqrtCthKernel<<<blocksPerGridArr2, threadsPerBlock>>>(arr1, M1);
        mapPiCbrtKernel<<<blocksPerGridArr2, threadsPerBlock>>>(arr2, arr2Copy, M2);
#ifdef  time_event
        cudaEventRecord(endStage2);
        cudaEventSynchronize(endStage2);
        cudaEventElapsedTime(&milliseconds, startStage2, endStage2);
        printf("\nTime of stage 2: %f ms\n", milliseconds);
#endif
#ifdef  DEBUG
        cudaMemcpy(arr1_host, arr1, M1 * sizeof(double), cudaMemcpyDeviceToHost);
        cudaMemcpy(arr2_host, arr2, M2 * sizeof(double), cudaMemcpyDeviceToHost);
        print_arr(arr1_host, M1);
        print_arr(arr2_host, M2);
#endif
#ifdef DEBUG
        printf("> arr2[0] = cbrt(arr2[0]*M_PI); \n");
#endif
        // Stage  3 - Merge multiply
#ifdef time_event
        cudaEventRecord(startStage3);
#endif
#ifdef DEBUG
        printf("> Stage 3 - Merge \n");
#endif
        multiplayKenrel<<<blocksPerGridArr2, threadsPerBlock>>>(arr1, arr2, M2);
#ifdef time_event
        cudaEventRecord(endStage3);
        cudaEventSynchronize(endStage3);
        cudaEventElapsedTime(&milliseconds, startStage3, endStage3);
        printf("\nTime of stage 3: %f ms\n", milliseconds);
#endif
#ifdef DEBUG
        printf("> Stage 3 - Merge is done ! \n");
#endif
#ifdef  DEBUG
        cudaMemcpy(arr2_host, arr2, M2 * sizeof(double), cudaMemcpyDeviceToHost);
            print_arr(arr2_host, M2);
#endif

        // Stage 5 - Reduce
#ifdef time_event
        cudaEventRecord(startStage5);
#endif
#ifdef DEBUG
        printf("> Stage 5 - Reduce \n");
#endif
        float sum = 0.0f;
        float *deviceSum;
        cudaMalloc((void**)&deviceSum, sizeof(float));

        cudaMemcpy(deviceSum, &sum, sizeof(float), cudaMemcpyHostToDevice);
        reduceKernel<<<blocksPerGridArr2, threadsPerBlock>>>(arr2, M2, deviceSum);
        cudaDeviceSynchronize();
#ifdef time_event
        cudaEventRecord(endStage5);
        cudaEventSynchronize(endStage5);
        cudaEventElapsedTime(&milliseconds, startStage5, endStage5);
        printf("\nTime of stage 5: %f ms\n", milliseconds);
#endif
#ifdef DEBUG
        printf("- Stage 5 - Reduce is done\n");
#endif

        float hostResult;
        cudaMemcpy(&hostResult, deviceSum, sizeof(float), cudaMemcpyDeviceToHost);
        cudaFree(deviceSum);
        printf("%f ", hostResult);
    }
    cudaEventRecord(end);
    cudaEventSynchronize(end);

    milliseconds = 0;
    cudaEventElapsedTime(&milliseconds, start, end);
    printf("\nExecution time of GPU: %f ms\n", milliseconds);

    cudaFree(arr1);
    cudaFree(arr2);
    cudaFree(arr2Copy);

    return 0;
}
