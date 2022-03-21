from time import sleep
from random import randint
from fei.ppds import Thread, Mutex, Semaphore, print

savage_number = 4
portion_number = 2
cooker_number = 4


class SimpleBarrier(object):
    def __init__(self, N):
        self.N = N
        self.cnt = 0
        self.mutex = Mutex()
        self.barrier = Semaphore(0)

    def wait(self, each=None, last=None):
        self.mutex.lock()
        if each:
            print(each)
        self.cnt += 1
        if self.cnt == self.N:
            if last:
                print(last)
            self.cnt = 0
            self.barrier.signal(self.N)
        self.mutex.unlock()
        self.barrier.wait()


class Shared(object):
    def __init__(self):
        self.servings = 0
        self.mutex = Mutex()
        self.emptyPot = Semaphore(0)
        self.fullPot = Semaphore(0)

        self.barrier1 = SimpleBarrier(savage_number)
        self.barrier2 = SimpleBarrier(savage_number)
        self.cooker_wait = SimpleBarrier(cooker_number)
        self.cookers = 0


def eat(sid):
    """
    Savage eating
    :param sid: id of savage
    :return: nothing
    """
    print(f"divoch {sid}: hodujem")
    sleep(0.2 + randint(0, 3) / 10)


def getServingFromPot(shared, sid):
    """
    Get food from table from savage
    :param shared: class contain all steering elements
    :param sid: id of savage
    :return: nothing
    """
    shared.servings -= 1
    print(f"divoch {sid}: zobral som si, zostatok porcii v hrnci je {shared.servings}")


def putServingsInPot(shared):
    """
    Put portions on table function
    :param shared: class contain all steering elements
    :return: nothing
    """
    print(f"kuchar: posledny")
    # time of putting on table
    sleep(0.5 + randint(0, 3) / 10)
    shared.servings += portion_number


def cook(shared, sid):
    """
    Code of cooking
    :param shared: class contain all steering elements
    :param sid: id of cooker
    :return: nothing
    """
    while True:
        shared.emptyPot.wait()
        # time of cooking
        sleep(0.5 + randint(0, 3) / 10)
        # barrier, all cookers wait one for another, next code doing in strict order, last cooker tell it is cooked
        shared.cooker_wait.wait(last="\n")
        # implementation of problem from lecture
        # ONLY ONE chef will tell the waiting savage that he is cooked
        shared.cookers += 1
        if shared.cookers == cooker_number:
            putServingsInPot(shared)
            # signal for savages
            shared.fullPot.signal()
            shared.cookers = 0


def savage(shared, sid):
    """
    Code of savage, contain take portion, eating, cooker wake up
    :param shared: class contain all steering elements
    :param sid: id of savage
    :return: nothing
    """
    # time of savage actions
    sleep(randint(0, 3) / 10)

    while True:
        shared.barrier2.wait(each=f"savage {sid}: pred vecerou",
                             last=f"savage {sid}: sme vsetci, zaciname hodovat")

        shared.mutex.lock()
        print(f"divoch {sid}: pocet porcii v hrnci je {shared.servings}")
        if shared.servings == 0:
            print(f"divoch {sid}: budim kuchara")
            # signal for all cookers
            shared.emptyPot.signal(cooker_number)
            shared.fullPot.wait()
        getServingFromPot(shared, sid)
        shared.mutex.unlock()
        eat(sid)
        shared.barrier1.wait(last="\n")


def run():
    shared = Shared()
    savages = [Thread(savage, shared, sid) for sid in range(savage_number)]

    cookers = [Thread(cook, shared, sid) for sid in range(cooker_number)]

    for s in savages+cookers:
        s.join()


if __name__ == "__main__":
    run()
