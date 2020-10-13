#include <string.h>
#include <stdlib.h>
#include "strings.h"

/*
 * Gets the user input directly and checks if it has
 * pipe, if pipe is given it will split all commands
 * up - thereafter / or if no pipe , the function
 * will begin tokenizing the command(s) and put them
 * into the the command array which is an array of
 * arrays of strings.
 * */
void handle_string(char* line, char ***command_array)
{
    //removing newline charactors
    size_t ln = strlen(line) - 1;
    if (*line&& line[ln] == '\n')
        line[ln] = '\0';

    //if pipe
    if (strstr(line,"|"))
    {
        char *commands[1024];
        tokenizer(line,"|",commands);
        int i = 0;
        for(int i=0; commands[i]!=NULL; i++)
        {
            command_array[i] = tkn_command(commands[i]);
        }
    }
    //if no pipe
    else
    {
        command_array[0] = tkn_command(line);
    }
}

/*
 * Allocates space for the string array which
 * holds the commands used by the shell.
 * */
char** tkn_command(char *line)
{
    char ** command = malloc(1024*sizeof(char*));
    for (int i = 0 ; i < 1024; ++i)
        command[i] = malloc(1024 * sizeof(char));
    tokenizer(line," ",command);
    return command;
}

/*
 * Takes a string and splits it up into parts
 * delimitted by a defined delimiter.
 * affects a pointer to a string array.
 * */
void tokenizer(char *command, char *delim, char *output[])
{
    int i=0;
    output[i] = strtok(command, delim);
    while(output[i] != NULL)
    {
        output[++i] = strtok(NULL, delim);
    }
}

/*
 * Freeing up all the arrays that have been
 * made in the tkn_command() function.
 * */
void freedom(char ***command_array)
{
    for(int i = 0; i>1024; i++){
        for(int j = 0; i>1024; i++){
            free(command_array[i][j]);
        }
        free(command_array[i]);
    }
}

