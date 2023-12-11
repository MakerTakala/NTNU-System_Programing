

#include <stdio.h>

#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include <fcntl.h>

/* Define some manifest constants to make the code more understandable */

#define ERR    (-1)             /* indicates an error condition */
#define READ   0                /* read end of a pipe */
#define WRITE  1                /* write end of a pipe */
#define STDIN  0                /* file descriptor of standard in */
#define STDOUT 1                /* file descriptor of standard out */


// ps aux|grep takala|wc>the_result
int main() {
    int pid_1, pid_2, pid_3;
    int pfd_1[2], pfd_2[2];

    if ( pipe(pfd_1) == ERR || pipe(pfd_2) == ERR ) {
        perror (" ");
        exit (ERR);
    }

    if (( pid_1 = fork () ) == ERR){
        perror (" ");
        exit (ERR);
    }
    if ( pid_1 != 0 ) {
        if (( pid_2 = fork () ) == ERR){
            perror (" ");
            exit (ERR);
        }
        if ( pid_2 != 0 ) {
            if ((pid_3 = fork() ) == ERR) {
                perror (" ");
                exit (ERR);
            }
            if (pid_3 != 0) {
                close ( pfd_1 [READ] );
                close ( pfd_1 [WRITE] );
                close ( pfd_2 [READ] );
                close ( pfd_2 [WRITE] );
                wait (( int * ) 0);
                wait (( int * ) 0);
                wait (( int * ) 0);
                wait (( int * ) 0);
            } else {
                close (STDIN);
                dup ( pfd_2 [READ] );
                close (STDOUT);
                int df = open("the_result",  O_WRONLY | O_CREAT | O_TRUNC, 0644);
                dup ( df );

                close ( pfd_1 [READ] );
                close ( pfd_1 [WRITE] );
                close ( pfd_2 [READ] );
                close ( pfd_2 [WRITE] );
                execlp("wc", "wc", NULL);
            }
        } else {
            close (STDIN);
            dup ( pfd_1 [READ] );
            close (STDOUT);
            dup ( pfd_2 [WRITE] );
            

            close ( pfd_1 [READ] );
            close ( pfd_1 [WRITE] );
            close ( pfd_2 [READ] );
            close ( pfd_2 [WRITE] );
            execlp("grep", "grep", "takala", NULL);
        }
    } else {
        close (STDOUT);
        dup ( pfd_1 [WRITE] );

        close ( pfd_1 [READ] );
        close ( pfd_1 [WRITE] );
        close ( pfd_2 [READ] );
        close ( pfd_2 [WRITE] );
        execlp("ps", "ps", "aux", NULL);
    }
    exit (0);
}

