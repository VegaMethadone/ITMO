#include <stdio.h>
#include "math.h"
#include "stdlib.h"
#include "sys/time.h"
#include "time.h"


int main() {
    int M1, M2, N;
    float A;

    for(int i = 0; i < 1; i++) {
        unsigned int seed = i;

        printf("Введите размерность массива M1: ");
        scanf("%d", &M1);
        printf("Введите диапазон для массива M1 (от 1 до A): ");
        scanf("%f", &A);
        M2 = M1 / 2;
        A *= 10-1;

        float *arr1 = malloc(M1 * sizeof(float));
        arr1[0] = 1.00;
        for (int j = 1; j < M1; j++) {
            int rand_num = rand_r(&seed);
            float rand_float = (float) rand_num / RAND_MAX;
            arr1[j] = (rand_float * A * 100) / 100;
        }

        float *arr2 = malloc(M2 * sizeof(float));
        arr2[0] = arr1[M1 - 1];
        for (int j = 1; j < M2; j++) {
            int rand_num = rand_r(&seed);
            float rand_float = (float) rand_num / RAND_MAX;
            arr2[j] = (rand_float * 9 * A + A) * 100 / 100;
        }

        printf("Массив M1:\n");
        for (int i = 0; i < M1; i++) {
            printf("%.2f ", arr1[i]);
        }
        printf("\n");

        printf("Массив M2:\n");
        for (int i = 0; i < M2; i++) {
            printf("%.2f ", arr2[i]);
        }
        printf("\n");

        // Освобождение памяти
        free(arr1);
        free(arr2);
    }
    /* Вывод массивов на экран
    printf("Массив M1:\n");
    for (int i = 0; i < M1; i++) {
        printf("%.2f ", arr1[i]);
    }
    printf("\n");

    printf("Массив M2:\n");
    for (int i = 0; i < M2; i++) {
        printf("%.2f ", arr2[i]);
    }
    printf("\n");

    
    free(arr1);
    free(arr2);
     */

    return 0;
}