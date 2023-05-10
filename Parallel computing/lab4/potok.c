#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>

void* print_progress(void* arg) {
    int* progress = (int*)arg;
    while (*progress < 100) {
        printf("Progress: %d%%\n", *progress);
        sleep(1);
    }
    pthread_exit(NULL);
}

int main() {
    int progress = 0;
    pthread_t thread;


    int result = pthread_create(&thread, NULL, print_progress, &progress);
    if (result != 0) {
        perror("Failed to create thread");
        exit(EXIT_FAILURE);
    }

  
    while (progress < 100) {
       
        
    }

    result = pthread_join(thread, NULL);
    if (result != 0) {
        perror("Failed to join thread");
        exit(EXIT_FAILURE);
    }
    printf("%d\n", progress);
    return EXIT_SUCCESS;
}