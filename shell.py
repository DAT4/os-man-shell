import re
from os import (
    execvp, # Start a command without specifying /bin/ + takes list(args)
    wait,   # Wait for child process to finish
    fork,   # Starts a child process
    close,  # Close channel direction
    pipe,   # Start pipe channel with in and out
    chdir,  # Changes the directory for parent and child
    dup2,   # Clones the in/out put of a NT
    write,
    read,
    getcwd,
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
    _exit(127) # This line is important to have or else the fork will not close.


def piping(cmd):
    reading, writing = pipe()
    pid = fork()
    if pid > CHILD:
        wait()
        close(writing)
        dup2(reading, STDIN)
        command(cmd[1])
    if pid == CHILD:
        close(reading)
        dup2(writing, STDOUT)
        command(cmd[0])
    else:
        print('Command not found:', cmd)


def normal(cmd):
    pid = fork()
    if pid > CHILD:
        wait()
    elif pid == CHILD:
        command(cmd)
    else:
        print('Command not found:', cmd)


def subprocess(cmd):
    if type(cmd[0]) == list:
        piping(cmd)
    else:
        normal(cmd)


def process(cmd):
    if 'cd' == cmd[0]:
        chdir(cmd[1])
    elif 'exit' == cmd[0]:
        exit()
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
            process(tokenize(input(f'mama@com - /{getcwd().split("/")[-1]} $ ')))
        except IndexError:
            pass
        except KeyboardInterrupt:
            print()
            continue
            


main()
