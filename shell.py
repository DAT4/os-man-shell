import re
from os import (
    execvp, # Start a command without specifying /bin/ + takes list(args)
    wait,   # Wait for child process to finish
    fork,   # Starts a child process
    close,  # Close channel direction
    pipe,   # Start pipe channel with in and out
    chdir,  # Changes the directory for parent and child
    dup2,   # Clones the in/out put of a NT
    getcwd, # Is used to get the users current working directory
)
from os import _exit

STDIN = 0
STDOUT = 1
STDERR = 2

CHILD = 0


def command(cmd):
    try:
        execvp(cmd[0].strip(), cmd)
    except OSError as e:
        print(e)


def pipechild(cmd, r1, w1):
    r2, w2 = pipe()
    pid2 = fork()
    if pid2 > CHILD:
        wait()
        close(w2)
        close(r1)
        dup2(r2, STDIN)
        dup2(w1, STDOUT)
        command(cmd[len(cmd)-1])
    elif pid2 == CHILD:
        if len(cmd) > 2:
            pipechild(cmd[:-1],r2,w2)
        else:
            close(r2)
            dup2(w2, STDOUT)
            command(cmd[0])
            _exit(0)


def piping(cmd):
    reading, writing = pipe()
    pid = fork()
    if pid > CHILD:
        wait()
        close(writing)
        dup2(reading, STDIN)
        command(cmd[len(cmd)-1])
        _exit(0)
    elif pid == CHILD:
        pipechild(cmd[:-1], reading, writing)
        _exit(0)
    else:
        _exit(0)


def normal(cmd):
    pid = fork()
    if pid > CHILD:
        wait()
    elif pid == CHILD:
        command(cmd)
        _exit(0)
    else:
        _exit(0)


def subprocess(cmd):
    pid = fork()
    if pid > CHILD:
        wait()
    elif pid == CHILD:
        if type(cmd[0]) == list:
            piping(cmd)
        else:
            normal(cmd)
        _exit(0)


def process(cmd):
    if 'cd' == cmd[0]:
        chdir(cmd[1])
    elif 'exit' == cmd[0]:
        exit(0)
    else:
        subprocess(cmd)


def tokenize(cmd):
    if '|' in cmd:
        cmd = [x.strip() for x in cmd.split('|')]
        cmd = [tokenize(x.strip()) for x in cmd]
        return cmd
    if re.search('\".*?\"', cmd):
        cmd = [x for x in cmd.split('"') if x]
        return cmd
    else:
        cmd = [x.strip() for x in cmd.split()]
        return cmd


def main():
    while True:
        try:
            directory   = getcwd().split("/")[-1]
            command     = input(f'.../{directory} % ')
            command     = tokenize(command)
            process(command)
        except IndexError:
            pass
        except KeyboardInterrupt:
            print()
            continue

main()
