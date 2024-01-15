#include "testhead.h"
#define MAX_LENGTH 256

char text[MAX_LENGTH];
char pattern[MAX_LENGTH];
int next[MAX_LENGTH];
int pattern_length;
int text_length;

// 计算部分匹配表（Next 数组）
void Next() {
    next[0] = -1;
    int i = 0;
    int j = -1;

    while (i < pattern_length - 1) {
        if (j == -1 || pattern[i] == pattern[j]) {
            i++;
            j++;
            next[i] = (pattern[i] == pattern[j]) ? next[j] : j;
        } else {
            j = next[j];
        }
    }
}

// KMP算法匹配
int kmp(int start) {
    int i = start;
    int j = 0;

    while (i < text_length && j < pattern_length) {
        if (j == -1 || text[i] == pattern[j]) {
            i++;
            j++;
        } else {
            j = next[j];
        }
    }

    return (j == pattern_length) ? i - j : -1;
}

int main() {
    printf("请输入主字符串:\n");
    fgets(text, sizeof(text), stdin);
    printf("请输入待匹配模式串:\n");
    fgets(pattern, sizeof(pattern), stdin);

    if (text[strlen(text) - 1] == '\n') {
        text[strlen(text) - 1] = '\0';
    }

    if (pattern[strlen(pattern) - 1] == '\n') {
        pattern[strlen(pattern) - 1] = '\0';
    }

    pattern_length = strlen(pattern);
    text_length = strlen(text);

    Next();

    int start = 0;
    int matched = 0;
    int pos;

    while (start < text_length) {
        pos = kmp(start);
        if (pos != -1) {
            printf("在位置%d处匹配\n", pos);
            start = pos + 1;
            matched = 1;
        } else {
            break;
        }
    }

    if (matched == 0) {
        printf("没有相匹配的位置\n");
    }

    return 0;
}