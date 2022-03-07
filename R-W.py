import datetime
from random import randint
from time import sleep

import matplotlib.pyplot as plt
import numpy as np
from fei.ppds import Thread, Semaphore, print, Mutex


class LS(object):
    def __init__(self):
        self.counter = 0
        self.mutex = Mutex()

    def lock(self, semaphore):
        self.mutex.lock()
        # if thread is first call wait on semaphore
        if not self.counter:
            semaphore.wait()
        self.counter += 1
        self.mutex.unlock()

    def unlock(self, semaphore):
        self.mutex.lock()
        self.counter -= 1
        # if thread is last call signal on semaphore
        if not self.counter:
            semaphore.signal()
        self.mutex.unlock()


class Shared:
    def __init__(self):
        self.room_empty = Semaphore(1)
        self.turn = Semaphore(1)
        self.ls = LS()


def writer_thread(thread_id, shared):
    for i in range(4):
        sleep(randint(0, 10) / 10)
        shared.turn.wait()
        shared.room_empty.wait()
        print(str(thread_id))
        sleep(0.3 + randint(0, 4) / 10)
        shared.room_empty.signal()
        shared.turn.signal()


def read_thread(thread_id, shared):
    for i in range(4):
        sleep(randint(0, 10) / 10)
        shared.turn.wait()
        shared.turn.signal()
        shared.ls.lock(shared.room_empty)
        print(str(thread_id))
        sleep(0.3 + randint(0, 4) / 10)
        shared.ls.unlock(shared.room_empty)


shared = Shared()
threads = []
graph = []

for w in [2, 5, 20]:
    for r in [5, 15, 7]:
        s = datetime.datetime.now()
        for i in range(w):
            t = Thread(writer_thread, f"Writer {i}", shared)
            threads.append(t)

        for i in range(r):
            t = Thread(read_thread, f"Reader {i}", shared)
            threads.append(t)

        for t in threads:
            t.join()

        e = datetime.datetime.now()
        time = e - s
        time = int(time.total_seconds() * 1000)

        graph.append([w, r, time])

fig = plt.figure()
ax = plt.axes(projection='3d')
x = np.array([x[0] for x in graph])
y = np.array([x[1] for x in graph])
z = np.array([x[2] for x in graph])
ax.set_xlabel("Read").set_ylabel("Write").set_zlabel("Time")
ax.plot_trisurf(x, y, z, cmap="viridis", edgecolor="none")
plt.show()
