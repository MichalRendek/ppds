"""
Copyright 2022 Michal Rendek
Licenced to MIT https://spdx.ogr/licenses/MIT.html

This module implements the solution for barber problem  without overtaking
"""


from time import sleep
from random import randint
from fei.ppds import Thread, Semaphore, Mutex, print


class Shared(object):
    """
    Class contain all steering elements
    """
    def __init__(self, chair_number):
        self.chair_number = chair_number
        self.customers = 0
        self.queue = []
        self.customer = Semaphore(0)
        self.customer_done = Semaphore(0)
        self.barber_done = Semaphore(0)
        self.mutex = Mutex()


def customer(shared, cid):
    """
    Function for manage costumer, cutting, wait in line, go out if is no chair
    :param shared: class contain all steering elements
    :param cid: id of customer for tracing
    """
    # initialize barrier for fifo implementation
    barber_barrier = Semaphore(0)
    while True:
        # try if is empty chair for customer
        shared.mutex.lock()
        print(f"Customer {cid} come")
        # if chair number and costumer number is same no chair is empty
        if shared.customers == shared.chair_number:
            print(f"Come {cid} but no chair")
            shared.mutex.unlock()
            # go out from barber shop
            balk()
            continue
        shared.customers += 1
        # print counter status
        print(f"Counter + {shared.customers}")
        # append uniq barrier of costumer for FIFO implementation
        shared.queue.append([barber_barrier, cid])
        shared.mutex.unlock()

        shared.customer.signal()
        barber_barrier.wait()

        getHairCut(cid)

        # wait until barber and costumer is done
        shared.customer_done.signal()
        shared.barber_done.wait()

        # in critical section countdown counter and tell who make it
        shared.mutex.lock()
        shared.customers -= 1
        print(f"Counter - {shared.customers}, countdown {cid}")
        shared.mutex.unlock()


def getHairCut(cid):
    """
    This function simulate cutting hair by barber in costumer function
    :param cid: id of customer for tracing
    """
    # print cutting customer
    print(f"Customer {cid} is cutting")
    # simulation of cutting
    sleep(0.2 + randint(0, 3) / 10)


def balk():
    """
    Function simulate costumer can be cut cause no chair
    """
    sleep(0.2 + randint(0, 3) / 10)


def barber(shared):
    """
    Function simulating barber, he cut in loop
    :param shared: class contain all steering elements
    """
    while True:
        # if customer is cutting, barber can cut anyone
        shared.customer.wait()
        # take uniq barrier of costumer and costumer id
        shared.mutex.lock()
        barber_barrier, cid = shared.queue.pop()
        shared.mutex.unlock()
        # signal that costumer can be cutting
        barber_barrier.signal()

        cutHair(cid)

        # wait until costumer is cut and barber finish cutting
        shared.customer_done.wait()
        shared.barber_done.signal()


def cutHair(cid):
    """
    This function simulate cutting hair by barber
    :param cid: is of customer for tracing
    """
    # print cutting customer
    print(f"Cutting {cid}")
    # simulation of cutting
    sleep(0.2 + randint(0, 3) / 10)


def run():
    # set number of customers and chairs
    customers_number = 4
    chair_number = 2

    # create threads
    shared = Shared(chair_number)
    barber_t = Thread(barber, shared)

    customers_t = [Thread(customer, shared, cid) for cid in range(customers_number)]

    barber_t.join()
    for s in customers_t:
        s.join()


if __name__ == "__main__":
    run()
