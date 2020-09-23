from re import search
from os import (
    execvp,
    wait,
    fork,
    close,
    pipe,
    chdir,
    dup2,
    getcwd,
    _exit,
)

STDIN   = 0
STDOUT  = 1
STDERR  = 2
CHILD   = 0

class Shell:
    '''A working linux shell with pipe functionality.'''

    def __init__(self):
        '''
        Looping forever and waiting for user input.

        The current working directory will be printed
        in front of each command the user is typing.
        '''
        while True:
            try:
                directory   = getcwd().split("/")[-1]
                command     = input(f'./{directory} % ')
                command     = self.tokenize(command)
                self.process(command)
            except IndexError:
                pass
            except KeyboardInterrupt:
                print()
                continue

    def tokenize(self, cmd):
        '''
        Lexing and parsing the string commands from the user.

        This is a partly recursive method that will call itself
        for each command in a pipe if there is a pipe, else it 
        will use regex to recognize strings and lastly it will
        split commands up in lists of strings divided by each
        space.
        '''
        if '|' in cmd:
            cmd = [x.strip() for x in cmd.split('|')]
            cmd = [self.tokenize(x.strip()) for x in cmd]
            return cmd
        if search('\".*?\"', cmd):
            cmd = [x for x in cmd.split('"') if x]
            return cmd
        else:
            cmd = [x.strip() for x in cmd.split()]
            return cmd

    def process(self, cmd):
        '''
        Figuring out if it is necessary to launch a child process.
        '''
        if 'cd' == cmd[0]:
            chdir(cmd[1])
        elif 'exit' == cmd[0]:
            _exit(0)
        else:
            pid = fork()
            if pid > CHILD:
                wait()
            elif pid == CHILD:
                if type(cmd[0]) == list:
                    self.piping(cmd)
                else:
                    self.command(cmd)
    
    def piping(self, cmd):
        '''
        Creates the first level of pipe channels, and executes the last
        command in parrent.
        '''
        reading, writing = pipe()
        pid = fork()
        if pid > CHILD:
            wait()
            close(writing)
            dup2(reading, STDIN)
            self.command(cmd[len(cmd)-1])
        elif pid == CHILD:
            self.pipechild(cmd[:-1], reading, writing)
            _exit(0)
        else:
            _exit(0)
    
    def pipechild(self, cmd, r1, w1):
        '''
        Pipes one to many commands and writes to outer scope pipe channel

        Method takes a list of commands and a full pipe, from outer scope, and 
        creates a child process in where it is checking and slicing the command 
        from the tail and recursivley calling itself, until the command is only 
        2 long, and at this point the last child process will execute the first
        command and the parrent processes in each recursivley called child process
        will use the file descriptors to read, insert into command and write to 
        the next command until all commands have been run through and in the end
        the output of all commands on the list will be collected in w1 from the
        outer scope of the method, which should be the piping() method.
        '''
        r2, w2 = pipe()
        pid = fork()
        if pid > CHILD:
            wait()
            close(w2)
            close(r1)
            dup2(r2, STDIN)
            dup2(w1, STDOUT)
            self.command(cmd[len(cmd)-1])
        elif pid == CHILD:
            if len(cmd) > 2:
                self.pipechild(cmd[:-1],r2,w2)
            else:
                close(r2)
                dup2(w2, STDOUT)
                self.command(cmd[0])
            _exit(0)
    
    def command(self, cmd):
        '''
        Ececutes a single command using os.execvp().

        If an error happens, like eg. command does not exist on the
        system then the error will be caught and printed.
        '''
        try:
            execvp(cmd[0].strip(), cmd)
        except OSError as e:
            print(e)
            _exit(0)
