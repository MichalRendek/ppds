# Exercuse two

## Description
Write program for implementation simple barrier which will solution for three tasks.
Program must run in Python 3.10.1

## Task 1
### Description 
Write a simple barrier form lecture scrap
### Solution 
Code was write from lecture scrap so here will be same similarities.
I create 5 threads and run their. Every thread call function barrier_example
which print thread id before barrier and after her. 

## Task 2
### Description
Write program including waiting every one thread before two functions in 
line.
### Solution 
First solution contains simple semaphore wait and signal functions 
with counter like as simple barrier. Firstly, counter increase while 
number of counter is number of threads. Then all threads pass through
double barrier. Second, counted decrease to zero, then pass through after 
ko function all threads again.
<hr>
Second solution contain simply same code but semaphore pass through 
after wait no one thread bud all in same time. This functionality is 
implement in semaphore core code.