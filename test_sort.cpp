#include <stdio.h>

int main() {
    int i;
    int num = 0;

    printf("请输入排序的整数个数:\n");
    scanf("%d", &num);

    // 使用常量或动态内存分配
    int arr[100];

    printf("请输入相应数量的整数:\n");
    for (i = 0; i < num; i++) {
        scanf("%d", &arr[i]);
    }

    for (int i = 0; i < num; i++) {
        for (int j = 0; j < num; j++) {
            if (arr[j] > arr[i]) {
                int temp = arr[i];
                arr[i] = arr[j];
                arr[j] = temp;
            }
        }
    }

    printf("排序好的数组为:\n");
    for (int i = 0; i < num; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");

    return 0;
}
