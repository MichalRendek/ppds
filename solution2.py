from random import randint
from time import sleep
from fei.ppds import Thread, Mutex
from collections import Counter


class Shared():
    def __init__(self, length):
        self.counter = 0
        self.end = length
        self.array = [0] * length


mutex = Mutex()


def counting(shared):
    # lock thread during all incrementations, all while, here running only one thread
    mutex.lock()
    while shared.counter < shared.end:
        shared.array[shared.counter] += 1
        # insert sleep in random time for random switching
        # between thread during counting
        sleep(randint(1, 10) / 1000)
        shared.counter += 1
    # after all incrementations unlock mutex
    mutex.unlock()


shared = Shared(1000)

t1 = Thread(counting, shared)
t2 = Thread(counting, shared)

t1.join()
t2.join()

counter = Counter(shared.array)
print(counter.most_common())
