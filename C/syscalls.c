#include "syscalls.h"

/*
 * The first sub process is created and if pipe is 
 * detected, then pipe function will be called or
 * else the normal execvp will just be called.
 * */
void process(char ***command_array)
{
    int pid = fork();
    if (pid > 0)
    {
        wait(0);
    }
    else if (pid == 0)
    {
        if (command_array[1] != NULL)
        {
            int i = 0;
            while(command_array[i] != NULL) i++;
            piping(command_array, --i, NULL);
        }
        else
        {
            execvp(command_array[0][0], command_array[0]);
            exit(127);
        }
    }
    else
    {
        exit(1);
    }
}

/*
 * This function, will start with the latest
 * command in the list of commands given to it, and then it will
 * use recursion to create all the neccesary pipes so that each
 * command is connected in a row of pipes, in the end, it will
 * execute each command from the first one to the last.
 * */
void piping(char ***command_array, int i, int *pipefd_outer)
{
    printf("%i",i);
    int pipefd[2];
    pipe(pipefd);
    int pid = fork();
    if (pid > 0)
    {
        wait(0);
        if (pipefd_outer != NULL)
        {
            close(pipefd_outer[0]);
            dup2(pipefd_outer[1], 1);
        }
        close(pipefd[1]);
        dup2(pipefd[0], 0);
        execvp(command_array[i][0], command_array[i]);
        exit(127);
    }
    else if (pid == 0)
    {
        if (i > 1)
        {
            piping(command_array, --i, pipefd);
            exit(0);
        }
        else
        {
            close(pipefd[0]);
            dup2(pipefd[1], 1);
            execvp(command_array[i-1][0], command_array[i-1]);
            exit(127);
        }
    }
    else
    {
        exit(1);
    }
}
