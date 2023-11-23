#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <stdlib.h>

int main() {
    int input_fd, output_fd;
    
    input_fd = open("foo.bar", O_RDONLY);
    
    if (input_fd < 0) {
        perror("open");
        exit(1);
    }

    output_fd = open("result", O_WRONLY | O_CREAT | O_TRUNC, 0644);
    if (output_fd < 0) {
        perror("open");
        exit(1);
    }

    close(STDIN_FILENO);
    dup(input_fd);
    close(input_fd);

    close(STDOUT_FILENO);
    dup(output_fd);
    close(output_fd);
   
    execlp("./a.out", NULL);

    return 0;
}
