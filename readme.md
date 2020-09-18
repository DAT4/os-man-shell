#Learn about system calls

## Fork
Fork creates a subprocess, or a child of the parent process. Fork and wait() works together. A fork function returns a pid (proccess id) which is a number. if PID is 0 then it is a child, if it is more than 0 then it is a parrent, and if it is less than 0 there is an error.

## Wait
Wait will wait for a fork to finish. There is also a waitpid() which will wait for a specific process with a specific id.

## Exec 
Exec is used to invoke subprocesses. 

## Write
Allows you to communicate with another user.

## Exit
This one is used to end the process


## File descriptors

The rest of the functions all have something to do with file descriptors.
* STDIN
* STDOUT
* STDERR


### Open
This one is used to open a file, the return value is a file descriptor.

### Close
Closes a file descriptor

### Read
This function will try to read from a file descriptor, and read it into a buffer.

### Pipe
This is used to create a unidirectional data channel for the parent and child processes to communicate. if successful pipe will return zero, else -1

# Design a simple command line shell for Linux

## The imports and the header

I imported only the **os** library, and the **re** library for dealing with regex.
From the **os** library i specifically imported the system calls which were relevant for the assignment

```python
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

```

I Declared some values for transparency

```python
STDIN = 0
STDOUT = 1
STDERR = 2

CHILD = 0


```

## The functions

### The main loop
```python
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
```

### The tokenizer


```python
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
```

### The identifier

```python
def process(cmd):
    if 'cd' == cmd[0]:
        chdir(cmd[1])
    elif 'exit' == cmd[0]:
        exit()
    else:
        subprocess(cmd)
```

### The subprocesses

#### First level subprocess

```python
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
```


#### No piping

```python
def normal(cmd):
    pid = fork()
    if pid > CHILD:
        wait()
    elif pid == CHILD:
        command(cmd)
        _exit(0)
    else:
        print('Command not found:', cmd)
        _exit(0)
```

#### Piping 

```python
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
    elif pid == CHILD:
        pipechild(cmd[:-1], reading, writing)
        _exit(0)
    else:
        _exit(0)
```

### The command

```python
def command(cmd):
    try:
        execvp(cmd[0].strip(), cmd)
    except OSError as e:
        print(e)
    _exit(127) # This line is important to have or else the fork will not close.

```
