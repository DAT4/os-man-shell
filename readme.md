# Learn about system calls

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

