# Exercise six

## Barber problem without overtaking
### Description 
Design a solution and model at least one of the synchronization issues discussed in the lecture in this module 
Barber problem without overtaking.
### Solution 
#### Code
In my case, I solved the problem using a FIFO queue where each user has their own barrier who controls the 
arrival in the barber.
<hr>
In first I create all threads and add functions inside.

>       customers_number = 4
>       chair_number = 2
>       
>       # create threads
>       shared = Shared(chair_number)
>       barber_t = Thread(barber, shared)
>       
>       customers_t = [Thread(customer, shared, cid) for cid in range(customers_number)]


Then I create customer as function. She had two arguments, id of customer thread and shader objects.
In FIFO solution I create simple barrier here.
Then customer try if chair is empty.
>       if shared.customers == shared.chair_number:
>           print(f"Come {cid} but no chair")
>           shared.mutex.unlock()
>           # go out from barber shop
>           balk()
>           continue

If customer can sit on chair append own barrier to shared object and start synchronize before cutting. 

>       shared.customer.signal()
>       barber_barrier.wait()

Then is cutting and barber can cut also. In barber costumer barrier is take and use like synchronize element.

>       # if customer is cutting, barber can cut anyone
>       shared.customer.wait()
>       # take uniq barrier of costumer and costumer id
>       shared.mutex.lock()
>       barber_barrier, cid = shared.queue.pop()
>       shared.mutex.unlock()
>       # signal that costumer can be cutting
>       barber_barrier.signal()

And on the end costumer and barber wait one to another, costumer countdown counter of fill chairs and code go again.

>       # wait until barber and costumer is done
>       shared.customer_done.signal()
>       shared.barber_done.wait()
>       
>       # in critical section countdown counter and tell who make it
>       shared.mutex.lock()
>       shared.customers -= 1
>       print(f"Counter - {shared.customers}, countdown {cid}")
>       shared.mutex.unlock()