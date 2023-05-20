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



int min(int x, int y) {
    if(x > y)
        return y;
    else 
        return x;
}

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

//stupid sort for dynamic
void dynamic_stupid_sort(double *array, int n) {
    //print_arr(array, n);
    int i = 0;
    while (i < n - 1) {
        if (array[i + 1] < array[i]) swap(array + i, array + i + 1), i = 0;
        else i++;
    }
    //print_arr(array, n);
}

//merge section
void merge(double *arr, int n){
    //print_arr(arr, n);
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
    //print_arr(arr, n);
    
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

    print_arr(arr, n);    
}



void dynamic_merge(double *arr, int done, int will_done, int current_chunk){
    double *restrict arr1 = malloc(done * sizeof(double));
    double *restrict arr2 = malloc(current_chunk * sizeof(double));
    double * restrict result = malloc((done + current_chunk) * sizeof(double));


    for(int i = 0; i < done; i++){
        arr1[i] = arr[i];
    }
    //printf("\nArr1 is: \n");
    //print_arr(arr1, done);


    int current = 0;
    for(int i = done; i < will_done; i++){
        arr2[current] = arr[i];
        current += 1;
        //printf(" arr[i] = %f", arr[i]);
    }
    //printf("\nArr2 is: \n");
    //print_arr(arr2, current_chunk);


    int l = 0;
    int r = 0;
    current = 0;

    while(l < done && r < current_chunk){
        if(arr1[l] < arr2[r]){
            result[current] = arr1[l];
            l += 1;
        } else {
            result[current] = arr2[r];
            r += 1;
        }
        current += 1;
    }

    while(l < done){
        result[current] = arr1[l];
        l += 1;
        current += 1;
    }

    while(r < current_chunk){
        result[current] = arr2[r];
        r += 1;
        current += 1;
    }


    //printf("\nResult is: \n");
    //print_arr(result, done + current_chunk);

    
    for(int i = 0; i < done + current_chunk; i++){
        arr[i] = result[i];
    }
    //printf("\nArr is: \n");
    //print_arr(arr, done + current_chunk);

    free(arr1);
    free(arr2);
    free(result);
}


// sort section for dynamic sort wich depends on k_threads 
void dynamic_parallel_sort(double *arr, int n, int k_threads){

    int chunk_size = 0;
    #pragma omp single
    {
        if(k_threads == 1) {
            chunk_size = n;
        } else {
            chunk_size = n / k_threads;
        }
    }
    //printf("\nChunk size is: %d\n", chunk_size);

    #pragma omp for
    {
        for(int i = 0; i < k_threads; i++){

            int done = chunk_size * i;
            //if we are in the end of arr. We can face with size problem of chunk cause chunk is bigger than arr remains
            // for this reason we use min function to understand  which size is smaller - chunk or n - strted part
            int current_chunk = min(n - done, chunk_size); 
            dynamic_stupid_sort(arr + done, current_chunk);
            
        }
    }
    //printf("Sorted arr is: \n");
    //print_arr(arr, n);

    #pragma omp single
    {
        for(int i = 1; i < k_threads; i++){
            int done = chunk_size * i;
            int current_chunk = min(n - done, chunk_size);
            int will_done = done + current_chunk;

            dynamic_merge(arr, done, will_done, current_chunk);
        }
    }
    

    //printf("final arr is : \n");
    //print_arr(arr, n);
   

}


int main(int argc, char *argv[]) {
    double start, end;
    start = omp_get_wtime();
    int k = 0;
    int progress __attribute__((unused));
    progress = 0;

    #pragma omp parallel sections num_threads(2) shared(k, progress)
    {
        #ifdef _OPENMP
            #pragma omp section
            {
                double time = 0;
                while (progress < 1) {
                    double time_temp = omp_get_wtime();
                    if (time_temp - time < 1) {
                        usleep(100);
                        continue;
                    }
                    printf("\nPROGRESS: %d\n", k);
                    time = time_temp;
                }
            }
        #endif

        #pragma omp section
        {

            unsigned int M1, M2;
            int A;
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
            
                double sum __attribute__((unused));
                sum = 0;
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
            
    
                

                #pragma omp parallel default(none) shared(M1, M2, arr1, arr2, arr2Coppy, A, seed, k, sum) 
                {
                    #pragma omp for
                    {
                        // Creating a coppy of the second array for the map creating stage       
                        for(int i = 0; i < M2; i++){
                            arr2Coppy[i] = arr2[i];
                        }
                    
                    }
                
                    #pragma omp for
                    {
                        // Stage 2 - Map creating by using sqrtf and cth
                        for(int i = 0; i < M1; i++){
                            arr1[i] = cosh(sqrt(arr1[i])) / sinh(sqrt(arr1[i]));
                        }
                        
                    }
                
                    #pragma omp for
                    {
                        // Modify the second array using M_PI and cbtrf
                        for(int i = 1; i < M2; i++){
                            arr2[i] = cbrt((arr2[i] + arr2Coppy[i-1]) * M_PI);
                        }
                        
                    }
                
                    arr2[0] = cbrt(arr2[0]*M_PI);
                    
                    #pragma omp for
                    {
                        // Stage 3 Merge multiply
                        for(int i = 0; i < M2; i++){
                            arr2[i] = arr1[i] * arr2[i];
                        }
                        
                    }
                    


                    // Stage 4 - Stupid sort
             
                    int k_threads __attribute__((unused)); 
                    k_threads = omp_get_num_procs();
                    if(k_threads == 2) { 
                        parallel_sort(arr2, M2);
                    } else {
                        dynamic_parallel_sort(arr2, M2, k_threads);
                    }
                    
                    
                    // Stage 5 Reduce
                    double min = arr2[0];

                    #pragma omp for reduction(+:sum) 
                    {
                        //#pragma omp parallel for reduction(+:sum)
                        for(int i = 0; i < M2; i++){
                            if(((int)arr2[i] / (int)min) % 2 == 0){
                                sum += sin(arr2[i]);
                            }
                        }
                    }

                    #pragma omp barrier
                }
                printf("%f ", sum);
            }
            progress = 1;
        }

    }   
    
    end = omp_get_wtime();
    printf("\n%d\n", (int)((end-start) * 1000.0));
    return 0;
    
}