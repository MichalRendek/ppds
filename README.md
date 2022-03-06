# Exercuse three

## Task 1
### Description 
Implement ADS Lightswitch with 2 methods lock and unlock
### Solution 
If thread is first that call methode lock, semaphore which is attribute of function,
call wait. Counter count threads which call this function for check it.

If thread is last that call methode unlock, semaphore which is attribute of function,
call signal. Counter count threads which call this function for check it.

## Task 2
### Description
### Solution 