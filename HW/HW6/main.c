#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <sys/wait.h>

void execute_commands() {
    pid_t pid = fork();

    if (pid == 0) {
        execlp("uptime", "uptime", NULL);
        execlp("who", "who", NULL);
        exit(0);
    } else if (pid > 0) {
        wait(NULL); 
    } else {
        perror("fork failed");
        exit(1);
    }
}

void handler(int sig) {
    if (sig == SIGINT) {
        execute_commands();
    } else if (sig == SIGALRM) {
        execute_commands();
        alarm(10);
    }
}

int main() {
    signal(SIGINT, handler);
    signal(SIGALRM, handler);

    alarm(10);

    while(1) {

    }
    return 0;
}
