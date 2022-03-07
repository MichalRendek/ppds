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
Read-Write problem
### Description
Implement read write problem in my case with a starvation problem. After that I answer
some questions.
### Solution 
Readers and writers are implementing as function which threads 
call. Threads are created in cycles. There we set more 
variants of number readers and writers and check time of running.
All this data are render in graph, and we see that more readers
and writers mean longer time of processing. There is fact, more
readers mean longer time than more writers.

### Questions
5. This problem can be to break already for one reader. 
    This occurs when the turnstile does not have a fifo queue implemented.
6. No. Writer lock the room one by one so here is no problem for reader take mutex
    and lock room for yourself.
7. If i good understand this problem, starvation is problem primary for reader 
    because writer is little faster than reader and if we have not fifo on 
    turnstile, writer will set turnstile still to wait and readers can't past 
    through.
8. Of course second is better, because if fifo, everyone has better chance take 
    access to data. In first code from lecture, starvation is something absolutely
    possible because readers can read in never ending loop in some case.
9. I think yes. More writers mean higher probability that writers pass through turnstile
    so access will be more balanced

     