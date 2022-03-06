from fei.ppds import Mutex


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
