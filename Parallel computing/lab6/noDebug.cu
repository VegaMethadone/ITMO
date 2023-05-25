#include <stdio.h>
#include <curand_kernel.h>

#define M_PI           3.14159265358979323846


//print section
void print_arr(double *arr, int n){
    for(int i = 0; i < n; i++)
    {
        printf("%f ", arr[i]);
    }
    printf("\n");
}

__global__ void randomKernel(unsigned int seed, double *array, int n, int A, int option){
    int tid = blockIdx.x;//blockIdx.x; // * blockDim.x + threadIdx.x;
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
    int tid =  blockIdx.x;//blockIdx.x; // * blockDim.x + threadIdx.x;
    if(tid < M2)
    {
        arr2Copy[tid] = arr2[tid];
    }
}

__global__ void mapSqrtCthKernel(double *arr1, int M1){
    int tid =  blockIdx.x;//blockIdx.x; //* blockDim.x + threadIdx.x;
    if(tid < M1)
    {
        arr1[tid] = sqrt(cosh(arr1[tid] / sinh(arr1[tid])));
    }
}

__global__ void mapPiCbrtKernel(double *arr2, double *arr2Copy, int M2){
    int tid =  blockIdx.x; //blockIdx.x; // * blockDim.x + threadIdx.x;
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
    int tid =  blockIdx.x; //blockIdx.x; // * blockDim.x + threadIdx.x;
    if(tid < M2)
    {
        arr2[tid] = arr1[tid] * arr2[tid];
    }
}


__global__ void reduceKernel(double *arr2, int M2, float *blockSums){

    int tid = blockIdx.x;//threadIdx.x; // + blockIdx.x * blockDim.x;

    if(tid < M2){
        if(((int)arr2[tid] / (int)arr2[0]) % 2 == 0)
        {
            atomicAdd(blockSums, (float) sin(arr2[tid]));
        }
    }
}


int main(){
    cudaError_t error = cudaGetLastError();
    cudaEvent_t start, end;
    cudaEventCreate(&start);
    cudaEventCreate(&end);

    int k = 0;

    int M1, M2;
    int A;
    //M1 = atoi(argv[1]);
    M1 = 806569;
    M2 = M1 / 2;
    A = 100;

    double *arr1;
    double *arr2;
    double *arr2Copy;

    cudaMalloc((void**)&arr1, M1 * sizeof (double ));
    cudaMalloc((void**)&arr2, M2 * sizeof(double ));
    cudaMalloc((void**)&arr2Copy, M2 * sizeof(double));
    if (error != cudaSuccess) {
        printf("CUDA error: %s\n", cudaGetErrorString(error));
    }

    int threadsPerBlock = 256;
    int blocksPerGridArr1 = (M1 + threadsPerBlock - 1) / threadsPerBlock;
    int blocksPerGridArr2 = (M2 + threadsPerBlock - 1) / threadsPerBlock;

    cudaEventRecord(start);
    if (error != cudaSuccess) {
        printf("CUDA error: %s\n", cudaGetErrorString(error));
    }
    for(k = 0; k< 100; k++){
        unsigned int seed = k;

        // Creating arrays
        randomKernel<<<blocksPerGridArr1, threadsPerBlock>>>(seed, arr1, M1, A, 1);
        randomKernel<<<blocksPerGridArr2, threadsPerBlock>>>(seed, arr2, M2, A, 2);
        copyKernel<<<blocksPerGridArr2, threadsPerBlock>>>(arr2, arr2Copy, M2);

        // Stage 2 - Map creating
        mapSqrtCthKernel<<<blocksPerGridArr2, threadsPerBlock>>>(arr1, M1);
        mapPiCbrtKernel<<<blocksPerGridArr2, threadsPerBlock>>>(arr2, arr2Copy, M2);

        // Stage  3 - Merge multiply
        multiplayKenrel<<<blocksPerGridArr2, threadsPerBlock>>>(arr1, arr2, M2);

        // Stage 5 - Reduce
        float sum = 0.0f;
        float *deviceSum;
        cudaMalloc((void**)&deviceSum, sizeof(float));

        cudaMemcpy(deviceSum, &sum, sizeof(float), cudaMemcpyHostToDevice);
        reduceKernel<<<blocksPerGridArr2, threadsPerBlock>>>(arr2, M2, deviceSum);
        cudaDeviceSynchronize();

        float hostResult;
        cudaMemcpy(&hostResult, deviceSum, sizeof(float), cudaMemcpyDeviceToHost);

        cudaFree(deviceSum);
        printf("%f ", hostResult);
    }
    cudaEventRecord(end);
    cudaEventSynchronize(end);

    float milliseconds = 0;
    cudaEventElapsedTime(&milliseconds, start, end);
    printf("\nExecution time of GPU: %f ms\n", milliseconds);

    cudaFree(arr1);
    cudaFree(arr2);
    cudaFree(arr2Copy);

    return 0;
}