#include "testhead.h"

int main() {
    int i;
    char c;
    int num = 0;

    printf("请输入排序的整数个数:\n");
    while ((c = getchar()) != '\n') {
        if (isdigit(c)) {
            num = num * 10 + (c - '0');
        } else {
            printf("无效输入，请重新输入一个整数\n");
            return 1; // Exit with an error code
        }
    }

    // 使用常量或动态内存分配
    int arr[100];

    printf("请输入相应数量的整数:\n");
    for (int i = 0; i < num; i++) {
        char d;
        int currentNum = 0;

        while ((d = getchar()) != '\n') {
            if (isdigit(d)) {
                currentNum = currentNum * 10 + (d - '0');
            } else {
                printf("无效输入（一次只能输入一个整数），请重新输入整数\n");
                return 1;
            }
        }
        arr[i] = currentNum;
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
