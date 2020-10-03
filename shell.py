from re import search
from os import execvp,wait,fork,close,pipe,chdir,dup2,getcwd,_exit
STDIN,STDOUT,STDERR,CHILD = 0,1,2,0

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
                command     = self.tokenize(input(f'./{directory} % '))
                self.process(command)
            except:
                pass

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
        elif 'help' == cmd[0]:
            pass
        else:
            self.subprocess(cmd)

    def subprocess(self, cmd):
        '''
        Launching a subprocess with fork, and check wheather to run pipe or not
        '''
        pid = fork()
        if pid > CHILD:
            wait()
        elif pid == CHILD:
            if type(cmd[0]) == list:
                self.pipe(cmd)
            else:
                self.command(cmd)
            _exit(0)
        else:
            _exit(0)

    def pipe(self, cmd, outer_reading=None, outer_writing=None):
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
        reading, writing = pipe()
        pid = fork()
        if pid > CHILD:
            wait()
            self.copy(writing,reading,STDIN)
            if outer_reading is not None: self.copy(outer_reading, outer_writing)
            self.command(cmd[len(cmd)-1])
        elif pid == CHILD:
            if len(cmd) > 2:
                self.pipe(cmd[:-1], reading, writing)
            else:
                self.copy(reading,writing)
                self.command(cmd[0])
            _exit(0)
        else:
            _exit(0)

    def copy(self, _close, _duplicate, fd=STDOUT):
        '''
        Closes one end of a pipe and uses the other end to copy data to a file descriptor
        '''
        close(_close)
        dup2(_duplicate, fd)
    
    def command(self, cmd):
        '''
        Ececutes a single command using os.execvp().

        If an error happens, like eg. command does not exist on the
        system then the error will be caught and printed.
        '''
        try:
            execvp(cmd[0].strip(), cmd)
        except OSError:
            print('Command not found.')
            _exit(0)

s = Shell()
