#include <stdio.h>

int main()
{
	int i, n=0;
	char a[999];
	char *p = a;
	printf("输入待检测字符串：");
	gets(a);
	while(a[n])n++;
	for(i = 0; *(p+i) == *(p + n - 1); i++) {
        n--;
    }
	if(n -i <= 2)  
        printf("该字符串回文yes\n");
	else
        printf("该字符串不回文no\n");
    return 0;
}
