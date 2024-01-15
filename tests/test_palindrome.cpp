#include "testhead.h"

int main()
{
	char s[100];
    printf("请输入字符串:\n");    
	fgets(s, sizeof(s), stdin);
    int len = strlen(s);
	if (s[len - 1] == '\n') {
        s[len - 1] = '\0';
		len--;
    }
    int mid = len / 2;
    for (int i = 0; i < len / 2; i++) {
        if (s[i] != s[len - 1 - i]) {
            printf("不是回文字符串\n");
            return 0;
        }
    }
    printf("是回文字符串\n");
    return 0;
}