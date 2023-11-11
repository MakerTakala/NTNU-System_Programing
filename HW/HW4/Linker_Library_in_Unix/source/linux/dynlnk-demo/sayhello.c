#include <stdio.h>

void sayhello(void)
{
   printf("\033[1;41m");
   printf("dynamic-linking library routine: HelloWorld!\n");
   printf("\033[0m");
}

