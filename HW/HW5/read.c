#include <stdio.h>
#include <ctype.h>

int main() {
    char input[1024];
    fgets(input, 1024, stdin);

    int inWord = 0;

    for (int i = 0; input[i] != '\0'; i++) {
        if (isalpha(input[i])) {
            if (!inWord) {
                putchar('(');
                inWord = 1;
            }
            putchar(input[i]);
        } else {
            if (inWord) {
                putchar(')');
                inWord = 0;
            }
            if (input[i] != '\n') {
                putchar(' ');
            }
        }
    }

    if (inWord) {
        putchar(')');
    }

    return 0;
}
