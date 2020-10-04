from re import search
from os import execvp,wait,fork,close,pipe,chdir,dup2,getcwd,_exit
STDIN,STDOUT,STDERR,CHILD = 0,1,2,0

def command(cmd):
    try:
        execvp(cmd[0].strip(), cmd)
    except OSError:
        print('Command not found.')
        _exit(0)

def copy(_close, _duplicate, fd=STDOUT):
    close(_close)
    dup2(_duplicate, fd)

def my_fork(parrent_stuff, child_stuff):
    pid = fork()
    if pid > CHILD:
        wait()
        parrent_stuff()
    elif pid == CHILD:
        child_stuff()
    else:
        _exit(0)

def my_pipe(cmd, outer_reading=None, outer_writing=None):
    reading, writing = pipe()
    pid = fork()
    if pid > CHILD:
        wait()
        copy(writing,reading,STDIN)
        if outer_reading is not None: copy(outer_reading, outer_writing)
        command(cmd[len(cmd)-1])
    elif pid == CHILD:
        if len(cmd) > 2:
            my_pipe(cmd[:-1], reading, writing)
        else:
            copy(reading,writing)
            command(cmd[0])
    else:
        _exit(0)

def process(cmd):
    if 'cd' == cmd[0]:
        chdir(cmd[1])
    elif 'exit' == cmd[0]:
        _exit(0)
    elif 'help' == cmd[0]:
        pass
    else:
        my_fork(lambda: None, lambda: my_pipe(cmd)) if type(cmd[0]) == list else my_fork(lambda:None, lambda: command(cmd))

def tokenize(cmd):
    if '|' in cmd:
        cmd = [x.strip() for x in cmd.split('|')]
        cmd = [tokenize(x.strip()) for x in cmd]
        return cmd
    if search('\".*?\"', cmd):
        cmd = [x for x in cmd.split('"') if x]
        return cmd
    else:
        cmd = [x.strip() for x in cmd.split()]
        return cmd

while True:
    try:
        directory   = getcwd().split("/")[-1]
        process(tokenize(input(f'./{directory} % ')))
    except IndexError:
        pass
