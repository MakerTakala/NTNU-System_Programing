#include <stdio.h>

void saygoodbye(void)
{
   printf("\033[1;32m");
   printf("static-linking library routine: Goodbye!\n");
   printf("\033[0m");
}

