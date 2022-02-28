from time import sleep
from random import randint
from fei.ppds import Thread, Mutex, Semaphore
from fei.ppds import print


class SimpleBarrier:
    def __init__(self, N):
        self.N = N
        self.C = 0
        self.S = Semaphore(0)
        self.M = Mutex()

    def wait(self):
        self.M.lock()
        self.C += 1
        if self.C == self.N:
            self.C = 0
            self.S.signal(self.N)
        self.M.unlock()
        self.S.wait()


def rendezvous(thread_name):
    sleep(randint(1, 10) / 10)
    print('rendezvous: %s' % thread_name)


def ko(thread_name):
    print('ko: %s' % thread_name)
    sleep(randint(1, 10) / 10)


def barrier_example(s1, s2, thread_name):
    while True:
        rendezvous(thread_name)
        s1.wait()
        ko(thread_name)
        s2.wait()


threads = list()
THREADS = 5
b1 = SimpleBarrier(THREADS)
b2 = SimpleBarrier(THREADS)

for i in range(THREADS):
    t = Thread(barrier_example, b1, b2, 'Thread %d' % i)
    threads.append(t)

for t in threads:
    t.join()
