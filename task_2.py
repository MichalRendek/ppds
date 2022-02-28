from time import sleep
from random import randint
from fei.ppds import Thread, Mutex, Semaphore
from fei.ppds import print


def rendezvous(thread_name):
    sleep(randint(1, 10) / 10)
    print('rendezvous: %s' % thread_name)


def ko(thread_name):
    print('ko: %s' % thread_name)
    sleep(randint(1, 10) / 10)


def barrier_example(thread_name):
    # this two variables are set as global for global connect to their
    global counter
    global THREADS

    while True:
        rendezvous(thread_name)
        m.lock()
        counter += 1
        if counter == THREADS:
            s1.signal(THREADS)
        m.unlock()
        s1.wait()

        ko(thread_name)

        m.lock()
        counter -= 1
        if counter == 0:
            s2.signal(THREADS)
        m.unlock()
        s2.wait()


threads = list()

m = Mutex()
s1 = Semaphore(0)
s2 = Semaphore(0)
counter = 0
THREADS = 5

for i in range(THREADS):
    t = Thread(barrier_example, 'Thread %d' % i)
    threads.append(t)

for t in threads:
    t.join()
