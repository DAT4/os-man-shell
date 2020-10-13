#include <stdio.h>
#include "strings.c"
#include "syscalls.c"

void command();
void printcwd();

/*
 * The main loop where the user inputs the commands
 * */
int main()
{
    while (1)
    {
        char line[1024] = "";
        char **command_array[1024] = {NULL};
        printcwd();
        fgets(line, 1024, stdin);
        handle_string(line, command_array);
        command(command_array);
        freedom(command_array);
    }
    return 0;
}

/*
 * will print the last folder in
 * the current working directory.
 * */
void printcwd()
{
    char *path[1024];
    char cwd[1024];
    getcwd(cwd, 1024);
    tokenizer(cwd, "/", path);
    int i = 0;
    while(path[i] != NULL) i++;
    printf("./%s %% ", path[i-1]);
}

/*
 * Here the command is validated.
 * */
void command(char ***command_array)
{
    if (strstr(command_array[0][0], "exit"))
    {
        exit(0);
    }
    else if (strstr(command_array[0][0], "cd"))
    {
        chdir(command_array[0][1]);
    }
    else
    {
        process(command_array);
    }
}
