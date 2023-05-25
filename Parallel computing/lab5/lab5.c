#include <math.h>
#include <stdio.h>
#include "stdlib.h"
#include "sys/time.h"
#include "time.h"
#include "string.h"
#include "unistd.h"
#include "pthread.h"
#include "omp.h"


//#define DEBUG_GENERATE  
//#define DEBUG_COPPY
//#define DEBUG_MAP
//#define DEBUG_MERGE
//#define DEBUG_SORT
//#define No_parallel
//#define DEBUG_REDUCE
//#define DEBUG_DYNAMIC
//#define DEBUG_CHUNK
//#define DEBUG

//#define SCHEDULE_DYNAMIC


double sum __attribute__((unused)) = 0;
int progress = 0;
int experements = 100;

typedef struct {
    double *array;
    int start;
    int end;
    unsigned int k;
    int A;
}generate_part_of_array;

typedef struct {
    double *arr2;
    double *arr2coppy;
    int start;
    int end;
}coppy_part_of_array;


typedef struct {
    double *array;
    int start;
    int end;
} work_with_array;

typedef struct {
    double *array_1;
    double *array_2;
    int start;
    int end;
}work_with_both;

typedef struct {
    double *array;
    int start;
    int end;
    double MIN;
    //double *Sum;
    pthread_mutex_t *mutex;
}work_with_one_with_min;

typedef struct{
    double *arr1;
    double *arr2;
    int chunk_size;
    int size_of_M2;
    int thread_id;
}sched_dynamic;


//swap section
void swap(double *x, double *y) {
    double tmp;
    tmp = *x;
    *x = *y;
    *y = tmp;
}

// Calculate optimal chunk size
int chunk_size(int size_of_array, int threads){
    int chunk_result = size_of_array / threads;
    return chunk_result;
}

// Print array by element
void print_arr(double *arr, int n){
    for(int i = 0; i < n; i++){
        printf("%f ", arr[i]);
    }
    printf("\n");
}

// Find min element
int min(int x, int y){
    return x < y ? x : y;
}

void *generate1(void *argv){
    #ifdef DEBUG_GENERATE
        printf("generate arr1 stage:\n");
    #endif

    generate_part_of_array *target = (generate_part_of_array *)argv;
    unsigned int seed = target->k;

    #ifdef DEBUG_GENERATE
        printf("start = %d\n", target->start);
        printf("end = %d\n", target->end);
        printf("Seed = %d\n", target->k);
        printf("A size is: %d\n", target->A);
    #endif

    for(int i = target->start; i < target->end; i++){
        target->array[i] = (rand_r(&seed) % (target->A * 100)) / 100.0 + 1;
    }

    #ifdef DEBUG_GENERATE
        for(int i = target->start; i < target->end; i++){
            printf("%f ", target->array[i]);
        }
        printf("\n");
    #endif

    pthread_exit(NULL);
}


void *generate2(void *argv){
    #ifdef DEBUG_GENERATE
        printf("generate arr2 stage:\n");
    #endif

    generate_part_of_array *target = (generate_part_of_array *)argv;
    unsigned int seed = target->k;

    #ifdef DEBUG_GENERATE
        printf("start = %d\n", target->start);
        printf("end = %d\n", target->end);
        printf("Seed = %d\n", target->k);
        printf("A size is: %d\n", target->A);
    #endif

    for(int i = target->start; i < target->end; i++){
        target->array[i] = target->A + rand_r(&seed) % (target->A * 9);
    }

    #ifdef DEBUG_GENERATE
        for(int i = target->start; i < target->end; i++){
            printf("%f ", target->array[i]);
        }
        printf("\n");
    #endif

    pthread_exit(NULL);       
}

void *coppy_arr(void *argv){
    #ifdef DEBUG_COPPY
        printf("Coppye the second array:\n");
    #endif

    coppy_part_of_array *target = (coppy_part_of_array *)argv;
    
    #ifdef DEBUG_COPPY
        printf("Start is: %d\n", target->start);
        printf("End is: %d\n", target->end);
    #endif

    for(int i = target->start; i < target->end; i++){
        target->arr2coppy[i] = target->arr2[i];
    }

    #ifdef DEBUG_COPPY
        for(int i = target->start; i < target->end; i++){
            printf("%f ", target->arr2coppy[i]);
        }
        printf("\n");
    #endif

    pthread_exit(NULL); 
}

void *map_qrtf_cth(void *argv){
    #ifdef DEBUG_MAP
        printf("Map qrtf_cth the first array:\n");
    #endif

    work_with_array *target = (work_with_array *)argv;

    #ifdef DEBUG_MAP
        printf("Start is: %d\n", target->start);
        printf("End is: %d\n", target->end);
    #endif

    for(int i = target->start; i < target->end; i++){
        target->array[i] = cosh(sqrt(target->array[i])) / sinh(sqrt(target->array[i]));
    }

    #ifdef DEBUG_MAP
        for(int i = target->start; i < target->end; i++){
            printf("%f ", target->array[i]);
        }
        printf("\n");
    #endif

    pthread_exit(NULL); 

}

void *map_cbrt_pi(void * argv){
    #ifdef DEBUG_MAP
        printf("Map cbrt_pi the second array:\n");
    #endif
    
    work_with_both *target = (work_with_both *)argv;

    #ifdef DEBUG_MAP
        printf("Start is: %d\n", target->start);
        printf("End is: %d\n", target->end);
    #endif

    for(int i = target->start + 1; i < target->end; i++){
        target->array_1[i] = cbrt((target->array_1[i] + target->array_2[i-1]) * M_PI);
    }

    #ifdef DEBUG_MAP
        for(int i = target->start; i < target->end; i++){
            printf("%f ", target->array_1[i]);
        }
        printf("\n");
    #endif

    pthread_exit(NULL);

}

// Merge section
void *merge(void *argv){
    #ifdef DEBUG_MERGE
        printf("Merge the second array:\n");
    #endif

    work_with_both *target = (work_with_both *)argv;

    #ifdef DEBUG_MERGE
        printf("Start is: %d\n", target->start);
        printf("End is: %d\n", target->end);
    #endif

    for(int i = target->start; i < target->end; i++){
        target->array_2[i] = target->array_1[i] * target->array_2[i];
    }

    #ifdef DEBUG_MERGE
        for(int i = target->start; i < target->end; i++){
            printf("%f ", target->array_2[i]);
        }
        printf("\n");
    #endif

    pthread_exit(NULL);

}

// Parallel section with mod from lab4 -2 threads
void *paralleling_sort(void *argv){
    #ifdef DEBUG_SORT
        printf("Sort section\n");
    #endif

    work_with_array *sort = (work_with_array *)argv;
    //stupid_sort(sort->array, sort->start, sort->end);
    int i = sort->start;
    while (i < sort->end - 1) {
        if (sort->array[i + 1] < sort->array[i]) swap(sort->array + i, sort->array + i + 1), i = sort->start;
        else i++;
    }

    #ifdef DEBUG_SORT
        for(int i = sort->start; i < sort->end; i++){
            printf("%f ", sort->array[i]);
        }
        printf("\n");
    #endif

    pthread_exit(NULL);
}


// Reduce section 
void *reduce_section(void *argv){
    #ifdef DEBUG_REDUCE
        printf("Reduce section\n");
    #endif

    double local_sum = 0;
    work_with_one_with_min *target = (work_with_one_with_min *)argv;

    #ifdef DEBUG_REDUCE
        printf("Start is: %d\n", target->start);
        printf("End is: %d\n", target->end);
    #endif

    for(int i = target->start; i < target->end; i++){
        if(((int)target->array[i] / (int)target->MIN) % 2 == 0){
            local_sum += sin(target->array[i]);
            
            #ifdef DEBUG_REDUCE
                printf("Target is += %f\n", target->array[i]);
                printf("sin(Target) is %f\n", sin(target->array[i]));
                printf("Local sum is %f\n", local_sum);
            #endif
        }
    }

    pthread_mutex_lock(target->mutex);
        sum += local_sum;
    pthread_mutex_unlock(target->mutex);

    #ifdef DEBUG_REDUCE
        printf("Sum is: %f\n", sum);
    #endif

    pthread_exit(NULL);
}


//merge section
void merge_arr(double *arr, int n){

    int chunk = chunk_size(n, 2);

    double arr1 [chunk];
    double arr2 [n - chunk];

    for(int i = 0; i < chunk; i++){
        arr1[i] = arr[i];
    }

    #ifdef DEBUG_SORT
        printf("Sort arr1:\n");
        print_arr(arr1, chunk);
    #endif

    int current = 0;
    for(int i = chunk; i < n; i++){
        arr2[current] = arr[i];
        current += 1;
    }

    #ifdef DEBUG_SORT
        printf("Sort arr2:\n");
        print_arr(arr2, n - chunk);
    #endif

    int n1 = chunk;
    int n2 = n-chunk;
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

void *progressBar(void *argv){
    double time = 0;
    while(progress < experements){
        double time_temp = omp_get_wtime();
        if(time_temp - time < 1){
            usleep(100);
            continue;
        }
        printf("\nPROGRESS: %d\n", progress);
        time = time_temp;
    }   
    pthread_exit(NULL);
}

pthread_mutex_t dynamic_mutex = PTHREAD_MUTEX_INITIALIZER;
int current_index = 0;

void *dynamicThreads(void *argv){
    sched_dynamic *target = (sched_dynamic *)argv;
    int start_index;
    int end_index;

    while(1){
        pthread_mutex_lock(&dynamic_mutex);
        start_index = current_index;
        current_index += target->chunk_size;
        pthread_mutex_unlock(&dynamic_mutex);

        if(start_index >= target->size_of_M2){
            return NULL;
        }

        end_index = (start_index + target->chunk_size) > target->size_of_M2 ? target->size_of_M2 : (start_index + target->chunk_size);

        for(int i = start_index; i < end_index; i++){
            target->arr2[i] = target->arr1[i] * target->arr2[i];
            #ifdef DEBUG_DYNAMIC
                printf("Thread %d: Processed index %d\n", target->thread_id, i);
            #endif
        }
    }
}

int main(int argc, char *argv[]){

    struct timeval T1, T2;
    long delta_ms;
    unsigned int k = 0;  
   
    unsigned int M1, M2;
    int A;
    int NTHREADS;
    M1 = atoi(argv[1]);
    M2 = M1 / 2;
    A = 100;
    NTHREADS = atoi(argv[2]);
    pthread_mutex_t mutex;
    
    #ifdef DEBUG
        printf("NTHREADS is %d\n", NTHREADS);
    #endif


    void *status;

    gettimeofday(&T1, NULL);

    // Allocate memmory for arrays
    double *restrict arr1 = malloc(M1 * sizeof(double));
    double *restrict arr2 __attribute__((unused)) = malloc(M2 * sizeof(double));
    double *restrict arr2coppy __attribute__((unused)) = malloc(M2 * sizeof(double));
    
    //progress section
    pthread_t progressThread;
    // Declarate nums of threads;
    pthread_t threads[NTHREADS];
    if(pthread_create(&progressThread, NULL, progressBar, NULL) == -1){
        printf("ProgressBar doesn't work correct [thread - %lu]",progressThread);
    }
    for(k = 0; k < experements; k++){
        current_index = 0;
        sum = 0;

        int chunk = chunk_size(M1, NTHREADS);
        #ifdef DEBUG
            printf("Chunk size of arr1 is: %d\n", chunk);
        #endif

        // Potential bag
        for(int i = 0; i < NTHREADS; i++){
            int done = chunk * i;
            int current_chunk = min(M1 - done, chunk);
            #ifdef DEBUG_CHUNK
                printf("Done is: %d\n", done);
            #endif       
            if(i == NTHREADS-1){
                #ifdef DEBUG_CHUNK
                    printf("Cheking size if chunk\n");
                #endif
                if(M1 - current_chunk != 0){
                    current_chunk = (M1 - done);
                    #ifdef DEBUG_CHUNK
                        printf("New size of chunk is %d\n", current_chunk);
                        printf("Start is: %d, End is: %d\n", done, current_chunk+done);
                    #endif
                }
            }
            // potential bag
            generate_part_of_array *generator = malloc(sizeof(generate_part_of_array));
            generator->array = arr1;
            generator->start = done;
            generator->end = done + current_chunk;
            generator->k = k;
            generator->A = A;

            #ifdef DEBUG_GENERATE
                printf("Iteration %d\n", i);
                printf("Start is: %d\n", generator->start );
                printf("End is: %d\n", generator->end);
                printf("Seed is: %d\n", generator->k);
                printf("A is: %d\n", generator->A);
            #endif

            //Creating POSIX threds
            if(pthread_create(threads + i, NULL, generate1, generator) == -1){
                printf("Thread %d is not created\n", i);
            }

        }
        //Merge pull threads
        for(int i = 0; i < NTHREADS; i++){
            if(pthread_join(threads[i], &status) == - 1){
                printf("Thread %lu does't work correct\n",threads[i]);
            }
            
        }
        #ifdef DEBUG_GENERATE
            printf("Merge pull threads\n");
        #endif


        #ifdef DEBUG_GENERATE
            printf("Print arr1 section\n");
            print_arr(arr1, M1);
        #endif

        // Generate Second array
        chunk = chunk_size(M2, NTHREADS);

        #ifdef DEBUG
            printf("Chunk size of arr2 is: %d\n", chunk);
        #endif

        for(int i = 0; i < NTHREADS; i++){
            int done = chunk * i;
            int current_chunk = min(M2 - done, chunk);
            #ifdef DEBUG_CHUNK
                printf("Done is: %d\n", done);
            #endif       
            if(i == NTHREADS-1){
                #ifdef DEBUG_CHUNK
                    printf("Cheking size if chunk\n");
                #endif
                if(M2 - current_chunk != 0){
                    current_chunk = (M2 - done);
                    #ifdef DEBUG_CHUNK
                        printf("New size of chunk is %d\n", current_chunk);
                        printf("Start is: %d, End is: %d\n", done, current_chunk+done);
                    #endif
                }
            }
            //coppy data in struct
            generate_part_of_array *generator = malloc(sizeof(generate_part_of_array));
            generator->array = arr2;
            generator->start = done;
            generator->end = done + current_chunk;
            generator->k = k;
            generator->A = A;

            #ifdef DEBUG_GENERATE
                printf("Iteration %d\n", i);
                printf("Start is: %d\n", generator->start );
                printf("End is: %d\n", generator->end);
                printf("Seed is: %d\n", generator->k);
                printf("A is: %d\n", generator->A);
            #endif

            // Creating POSIX threads
            if(pthread_create(threads + i, NULL, generate2, generator) == -1){
                printf("Thread %d is not created\n", i);
            }
        }
        // Merge pull threads
        for(int i = 0; i < NTHREADS; i++){
            if(pthread_join(threads[i], &status) == -1){
                printf("Thread %lu doesn't work correct\n",threads[i]);
            }
        }
        #ifdef DEBUG_GENERATE
            printf("Merge pull threads\n");
        #endif

        #ifdef DEBUG_GENERATE
            printf("Print arr 2 section\n");
            print_arr(arr2, M2);
        #endif

        // Coppy of the second Array section
        for(int i = 0; i < NTHREADS; i++){
            int done = chunk * i;
            int current_chunk = min(M2 - done, chunk);
            #ifdef DEBUG_CHUNK
                printf("Done is: %d\n", done);
            #endif       
            if(i == NTHREADS-1){
                #ifdef DEBUG_CHUNK
                    printf("Cheking size if chunk\n");
                #endif
                if(M2 - current_chunk != 0){
                    current_chunk = (M2 - done);
                    #ifdef DEBUG_CHUNK
                        printf("New size of chunk is %d\n", current_chunk);
                        printf("Start is: %d, End is: %d\n", done, current_chunk+done);
                    #endif
                }
            }

            coppy_part_of_array *copyrator = malloc(sizeof(coppy_part_of_array));
            copyrator->arr2 = arr2;
            copyrator->arr2coppy = arr2coppy;
            copyrator->start = done;
            copyrator->end = done + current_chunk;

            #ifdef DEBUG_COPPY
                printf("Start is %d\n", copyrator->start);
                printf("End is %d\n", copyrator->end);
            #endif

            // Creating POSIX threads
            if(pthread_create(threads + i, NULL, coppy_arr, copyrator) == -1){
                printf("Coppy thread %lu doesn't work correct\n", threads[i]);
            }
        }

        #ifdef DEBUG_COPPY
            printf("Merge Coppy pull threads\n");
        #endif

        #ifdef DEBUG_COPPY
            printf("Print arr2coppy section\n");
            print_arr(arr2coppy, M2);
        #endif

        // Map section sqrt & cth
        chunk = chunk_size(M1, NTHREADS);
        for(int i = 0; i < NTHREADS; i++){
            int done = chunk * i;
            int current_chunk = min(M1 - done, chunk);
            #ifdef DEBUG_CHUNK
                printf("Done is: %d\n", done);
            #endif       
            if(i == NTHREADS-1){
                #ifdef DEBUG_CHUNK
                    printf("Cheking size if chunk\n");
                #endif
                if(M1 - current_chunk != 0){
                    current_chunk = (M1 - done);
                    #ifdef DEBUG_CHUNK
                        printf("New size of chunk is %d\n", current_chunk);
                        printf("Start is: %d, End is: %d\n", done, current_chunk+done);
                    #endif
                }
            }

            work_with_array *maping = malloc(sizeof(work_with_array));
            maping->array = arr1;
            maping->start = done;
            maping->end = done + current_chunk;

            #ifdef DEBUG_MAP
                printf("Start is: %d\n", maping->start);
                printf("End is: %d\n", maping->end);
            #endif


            // Creating POSIX threads
            if(pthread_create(threads + i, NULL, map_qrtf_cth, maping) == -1){
                printf("Map sqrt & cth thread %lu doesn't work correct\n", threads[i]);
            }
        }
        // Merge pull threads
        for(int i = 0; i < NTHREADS; i++){
            if(pthread_join(threads[i], &status) == -1){
                printf("Thread %lu doesn't work correct\n",threads[i]);
            }
        }

        #ifdef DEBUG_MAP
            printf("Merge Map pull threads\n");
        #endif

        #ifdef DEBUG_MAP
            printf("Print arr1 section\n");
            print_arr(arr1, M1);
        #endif
        
        // Map section cbrt * M_PI
        chunk = chunk_size(M2, NTHREADS);
        for(int i = 0; i < NTHREADS; i++){
            int done = chunk * i;
            int current_chunk = min(M2 - done, chunk);
            #ifdef DEBUG_CHUNK
                printf("Done is: %d\n", done);
            #endif       
            if(i == NTHREADS-1){
                #ifdef DEBUG_CHUNK
                    printf("Cheking size if chunk\n");
                #endif
                if(M2 - current_chunk != 0){
                    current_chunk = (M2 - done);
                    #ifdef DEBUG_CHUNK
                        printf("New size of chunk is %d\n", current_chunk);
                        printf("Start is: %d, End is: %d\n", done, current_chunk+done);
                    #endif
                }
            }

            work_with_both *maping = malloc(sizeof(work_with_both));
            maping->array_1 = arr2;
            maping->array_2 = arr2coppy;
            maping->start = done;
            maping->end = done + current_chunk;

            #ifdef DEBUG_MAP
                printf("Start is: %d\n", maping->start);
                printf("End is: %d\n", maping->end);
            #endif

            // Creating POSIX threads
            if(pthread_create(threads + i, NULL, map_cbrt_pi, maping) == -1){
                printf("Map cbrt & pi thread %lu doesn't work correct\n", threads[i]);
            }
        }
        // Merge pull threads
        for(int i = 0; i < NTHREADS; i++){
            if(pthread_join(threads[i], &status) == -1){
                printf("Thread %lu doesn't work correct\n",threads[i]);
            }
        }

        // Working with exception
        arr2[0] = cbrt(arr2[0]*M_PI);

        #ifdef DEBUG_MAP
            printf("Merge Map pull threads\n");
        #endif

        #ifdef DEBUG_MAP
            printf("Print arr2 after mapping section\n");
            print_arr(arr2, M2);
        #endif
        


        // Merge sction
        #ifdef SCHEDULE_DYNAMIC
            chunk = chunk_size(M2, NTHREADS);
            chunk /= 10;
            for(int i = 0; i < NTHREADS; i++){
                sched_dynamic * merging = malloc(sizeof(sched_dynamic));

                merging->arr1 = arr1;
                merging->arr2 = arr2;
                merging->chunk_size = chunk;
                merging->size_of_M2 = M2;
                merging->thread_id = i;

                #ifdef DEBUG_DYNAMIC
                    printf("Chunk size is: %d\n", merging->chunk_size);
                    printf("Size if M2 is: %d\n", merging->size_of_M2);
                    printf("Thread id is: %d\n", merging->thread_id);
                #endif

                if(pthread_create(threads + i, NULL, dynamicThreads, merging) == -1){
                    printf("Merge thread %lu doesn't work correct\n", threads[i]);
                }
            }
            // Merge pull threads
            for(int i = 0; i < NTHREADS; i++){
                if(pthread_join(threads[i], &status) == -1){
                    printf("Thread %lu doesn't work correct\n",threads[i]);
                }
            }
            #ifdef DEBUG_DYNAMIC
                printf("Merge Map pull threads\n");
            #endif

            #ifdef DEBUG_DYNAMIC
                printf("Print arr2 after merge section\n");
                print_arr(arr2, M2);
            #endif
        #else
            for(int i = 0; i < NTHREADS; i++){
                int done = chunk * i;
                int current_chunk = min(M2 - done, chunk);
                #ifdef DEBUG_CHUNK
                    printf("Done is: %d\n", done);
                #endif       
                if(i == NTHREADS-1){
                    #ifdef DEBUG_CHUNK
                        printf("Cheking size if chunk\n");
                    #endif
                    if(M2 - current_chunk != 0){
                        current_chunk = (M2 - done);
                        #ifdef DEBUG_CHUNK
                            printf("New size of chunk is %d\n", current_chunk);
                            printf("Start is: %d, End is: %d\n", done, current_chunk+done);
                        #endif
                    }
                }

                work_with_both *merging = malloc(sizeof(work_with_both));
                merging->array_1 = arr1;
                merging->array_2 = arr2;
                merging->start = done;
                merging->end = done + current_chunk;

                #ifdef DEBUG_MERGE
                    printf("Start is: %d\n", merging->start);
                    printf("End is: %d\n", merging->end);
                #endif

                if(pthread_create(threads + i, NULL, merge, merging) == -1){
                    printf("Merge thread %lu doesn't work correct\n", threads[i]);
                }
            }
        // Merge pull threads
            for(int i = 0; i < NTHREADS; i++){
                if(pthread_join(threads[i], &status) == -1){
                    printf("Thread %lu doesn't work correct\n",threads[i]);
                }
            }
            #ifdef DEBUG_MERGE
                printf("Merge Map pull threads\n");
            #endif

            #ifdef DEBUG_MERGE
                printf("Print arr2 after merge section\n");
                print_arr(arr2, M2);
            #endif
        #endif
        


        //Sort section
        // signal
        chunk = chunk_size(M2, 2);
        for(int i = 0; i < 2; i++){
            int done = chunk * i;
            int current_chunk = min(M2 - done, chunk);
            #ifdef DEBUG_CHUNK
                printf("Done is: %d\n", done);
            #endif       
            if(i == NTHREADS-1){
                #ifdef DEBUG_CHUNK
                    printf("Cheking size if chunk\n");
                #endif
                if(M2 - current_chunk != 0){
                    current_chunk = (M2 - done);
                    #ifdef DEBUG_CHUNK
                        printf("New size of chunk is %d\n", current_chunk);
                        printf("Start is: %d, End is: %d\n", done, current_chunk+done);
                    #endif
                }
            }

            work_with_array *sort = malloc(sizeof(work_with_array));
            sort->array = arr2;
            sort->start = done;
            sort->end = done + current_chunk;

            #ifdef DEBUG_SORT
                printf("Start is: %d\n", sort->start);
                printf("End is: %d\n", sort->end);
            #endif

             if(pthread_create(threads + i, NULL, paralleling_sort, sort) == -1){
                printf("Sort thread %lu doesn't work correct\n", threads[i]);
            }
        }
        // Merge pull threads
        for(int i = 0; i < 2; i++){
            if(pthread_join(threads[i], &status) == -1){
                printf("Thread %lu doesn't work correct\n",threads[i]);
            }
        }
        #ifdef DEBUG_SORT
            printf("Sort Map pull threads\n");
        #endif

        merge_arr(arr2, M2);

        #ifdef DEBUG_SORT
            printf("Print arr2 after sort section\n");
            print_arr(arr2, M2);
        #endif


        #ifdef No_parallel
            print_arr(arr2, M2);
            for(int i = 0; i < M2; i++){
                if(((int)arr2[i]/(int)arr2[0]) % 2 == 0){
                    sum += sin(arr2[i]);
                }
            }
        #else
            // Reduce Section
            // Work with exception 
            double MIN = arr2[0];
            pthread_mutex_init(&mutex, NULL);

            chunk = chunk_size(M2, NTHREADS);
            for(int i = 0; i < NTHREADS; i++){
                int done = chunk * i;
                int current_chunk = min(M2 - done, chunk);
                #ifdef DEBUG_CHUNK
                    printf("Done is: %d\n", done);
                #endif       
                if(i == NTHREADS-1){
                    #ifdef DEBUG_CHUNK
                        printf("Cheking size if chunk\n");
                    #endif
                    if(M2 - current_chunk != 0){
                        current_chunk = (M2 - done);
                        #ifdef DEBUG_CHUNK
                            printf("New size of chunk is %d\n", current_chunk);
                            printf("Start is: %d, End is: %d\n", done, current_chunk+done);
                        #endif
                }
            }

                work_with_one_with_min *reduce = malloc(sizeof(work_with_one_with_min));
                reduce->array = arr2;
                reduce->start = done;
                reduce->end = done + current_chunk;
                reduce->MIN = MIN;
                //reduce->Sum = &sum;
                reduce->mutex = &mutex;

                #ifdef DEBUG_REDUCE
                    printf("Start is: %d\n", reduce->start);
                    printf("End is: %d\n", reduce->end);
                    printf("MIN is: %f\n", reduce->MIN);
                #endif

                if(pthread_create(threads + i, NULL, reduce_section, reduce) == -1){
                    printf("Sort thread %lu doesn't work correct\n", threads[i]);
                }
            }
            // Merge pull threads
            for(int i = 0; i < NTHREADS; i++){
                if(pthread_join(threads[i], &status) == -1){
                    printf("Thread %lu doesn't work correct\n",threads[i]);
                }
            }
            #ifdef DEBUG_REDUCE
                printf("Reduce Map pull threads\n");
            #endif

        #endif
        printf("%f ", sum);
        pthread_mutex_destroy(&mutex);
        progress++;
    }
    pthread_join(progressThread, NULL);
    free(arr1);
    free(arr2);
    free(arr2coppy);

    gettimeofday(&T2, NULL);
    delta_ms = 1000*(T2.tv_sec - T1.tv_sec) + (T2.tv_usec - T1.tv_usec) / 1000;
    printf("\n%ld\n", delta_ms);
    pthread_exit(NULL);
}
