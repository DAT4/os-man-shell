#include <stdio.h>
#include "strings.c"
#include "syscalls.c"

void command();

/*
 * The main loop where the user inputs the commands
 * */
int main()
{
    while (1)
    {
        char line[1024] = "";
        char **command_array[1024] = {NULL};
        fgets(line, 1024, stdin);
        handle_string(line, command_array);
        command(command_array);
        freedom(command_array);
    }
    return 0;
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
        char out[1024];
        chdir(command_array[0][1]);
        getcwd(out, 1024);
    }
    else
    {
        process(command_array);
    }
}
