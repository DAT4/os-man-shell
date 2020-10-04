from re import search
from os import execvp,wait,fork,close,pipe,chdir,dup2,getcwd,_exit
STDIN,STDOUT,STDERR,CHILD = 0,1,2,0

def command(cmd):
    try: execvp(cmd[0].strip(), cmd)
    except OSError: print('Command not found.')
    finally: _exit(0)

def copy(_close, _duplicate, fd=STDOUT):
    close(_close)
    dup2(_duplicate, fd)

def my_fork(child_stuff, parrent_stuff=lambda:None):
    pid = fork()
    if pid > CHILD: wait(); parrent_stuff()
    elif pid == CHILD: child_stuff()
    else: _exit(0)

def my_pipe(cmd, outer_reading=None, outer_writing=None):
    def child_stuff():
        copy(writing,reading,STDIN)
        if outer_reading is not None: copy(outer_reading, outer_writing)
        command(cmd[len(cmd)-1])
    def parrent_stuff():
        if len(cmd) > 2: my_pipe(cmd[:-1], reading, writing)
        else: copy(reading,writing); command(cmd[0])
    reading, writing = pipe()
    my_fork(parrent_stuff,child_stuff)

def process(cmd):
    if 'cd' == cmd[0]: chdir(cmd[1])
    elif 'exit' == cmd[0]: exit(0)
    else: my_fork(lambda: my_pipe(cmd)) if type(cmd[0]) == list else my_fork(lambda: command(cmd))

def tokenize(cmd):
    if '|' in cmd: return [tokenize(x.strip()) for x in [x.strip() for x in cmd.split('|')]]
    elif search('\".*?\"', cmd): return [x for x in cmd.split('"') if x]
    else: return [x.strip() for x in cmd.split()]

while True:
    try: process(tokenize(input(f'./{getcwd().split("/")[-1]} % ')))
    except IndexError: pass
