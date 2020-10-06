'''The comments are found in the readme.md under "Implementation"'''
from re import search
from os import execvp,wait,fork,close,pipe,chdir,dup2,getcwd,_exit
STDIN,STDOUT,CHILD = 0,1,0

def command(cmd):
    try: execvp(cmd[0].strip(), cmd)
    except OSError: print('Command not found.'); _exit(127)

def copy(_close, _duplicate, fd=STDOUT):
    close(_close)
    dup2(_duplicate, fd)

def my_fork(child, parrent=lambda:None):
    pid = fork() 
    if pid > CHILD: wait(); parrent()
    elif pid == CHILD: child()
    else: _exit(127)

def my_pipe(cmd, _r=None, _w=None):
    def parrent():
        if _r is not None: copy(_r, _w)
        copy(w,r,STDIN); command(cmd[len(cmd)-1])
    def child(): 
        if len(cmd) > 2: my_pipe(cmd[:-1], r, w)
        else: copy(r,w); command(cmd[0])
    r, w = pipe()
    my_fork(child,parrent)

def process(cmd):
    if 'cd' == cmd[0]: chdir(cmd[1])
    elif 'exit' == cmd[0]: exit(0)
    else: my_fork(lambda: my_pipe(cmd)) if type(cmd[0]) == list else my_fork(lambda: command(cmd))

def tokenize(cmd):
    if '|' in cmd: return [tokenize(x.strip()) for x in [x.strip() for x in cmd.split('|')]]
    elif search('(\'.*?\')', cmd): return [x for x in cmd.split("'") if x]
    else: return [x.strip() for x in cmd.split()]

while True:
    try: process(tokenize(input(f'./{getcwd().split("/")[-1]} % ')))
    except IndexError: pass
