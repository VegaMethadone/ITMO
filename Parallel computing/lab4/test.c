#include <stdio.h>
#include <stdlib.h>
#include <omp.h>


void print_arr(double *arr, int n){
    for(int i = 0; i < n; i++){
        printf("%f ", arr[i]);
    }
    printf("\n");
}

void swap(double *x, double *y) {
    double tmp;
    tmp = *x;
    *x = *y;
    *y = tmp;
}

void stupid_sort(double *array, int l, int r) {
    int i = l;
    while (i < r - 1) {
        if (array[i + 1] < array[i]) swap(array + i, array + i + 1), i = l;
        else i++;
    }
}


void merge(double *arr, int n){
    double arr1 [n/2];
    double arr2 [n - n/2];

    for(int i = 0; i < n/2; i++){
        arr1[i] = arr[i];
    }
    print_arr(arr1, n/2);
    int current = 0;
    for(int i = n/2; i < n; i++){
        arr2[current] = arr[i];
        current += 1;
    }
    print_arr(arr2, n - n/2);

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


void parallel_sort(double *arr, int n){

    #pragma omp parallel section
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

int main(int argc, char *argv[]) {

    double start, end;

    int progress = 0;

    #pragma omp parallel sections num_threads(2) shared(i, finished)
    {
        #ifdef _OPENMP
            #pragma omp section
            {
                double time = 0;
                while(progress < 1) {
                    double time_temp = omp_get_wtime();
                    if(time_temp - time < 1) {
                        usleep(100);
                        continue;
                    };
                    printf("\nPROGRESS: %d\n", i);
                    time = time_temp;
                }
            }
        #endif    
    }   


    start = omp_get_wtime();

    int n = atoi(argv[1]);
    
    double *restrict arr = malloc(n * sizeof(double));

    for(unsigned int i = 0; i < n; i++){
        unsigned int seed = i;
        arr[i] = (rand_r(&seed) % (77 * 100)) / 100.0 + 1;
    }
    print_arr(arr, n);
    printf("\n");
    printf("\n");
    printf("\n");

    parallel_sort(arr, n);


    end = omp_get_wtime();
    printf("%f ", (end - start) * 1000.0);
    return 0;
}