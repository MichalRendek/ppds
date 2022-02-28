from random import randint
from time import sleep
from fei.ppds import Thread, Semaphore, Mutex
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


def barrier_example(barrier, thread_id):
    # insert sleep in random time for random wait
    # until thread print status
    sleep(randint(1, 10) / 10)
    print("vlakno %d pred barierou" % thread_id)
    barrier.wait()
    print("vlakno %d po bariere" % thread_id)


sb = SimpleBarrier(5)

threads = [Thread(barrier_example, sb, i) for i in range(5)]
[t.join() for t in threads]
