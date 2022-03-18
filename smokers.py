from time import sleep
from random import randint
from fei.ppds import Thread, Semaphore, Mutex, print


class Shared(object):
    """
    Contain all steering elements
    """
    def __init__(self):
        self.tobacco = Semaphore(0)
        self.paper = Semaphore(0)
        self.matches = Semaphore(0)

        self.pusherTobacco = Semaphore(0)
        self.pusherPaper = Semaphore(0)
        self.pusherMatches = Semaphore(0)

        self.mutex = Mutex()
        self.isTobacco = 0
        self.isMatches = 0
        self.isPaper = 0

        # helper variables for find resolution of problem from lecture (the problem of favoring smokers)
        self.tobaccoCounter = 0
        self.matchesCounter = 0
        self.paperCounter = 0

        self.agentSem = Semaphore(1)


def make_cigarette(name):
    """
    Function simulate code for making cigarette
    :param name: unlimited smoker product
    :return: nothing
    """
    print(f"smoker '{name}' makes cigarette")
    sleep(randint(0, 10) / 100)


def smoke(name):
    """
    Function simulate smoking cigarette
    :param name: unlimited smoker product
    :return: nothing
    """
    print(f"smoker '{name}' smokes")
    sleep(randint(0, 10) / 100)


def smoker_matches(shared):
    """
    Function represented smoking of smoker with matches
    :param shared: class contain all steering elements
    :return: nothing
    """
    while True:
        sleep(randint(0, 10) / 100)
        # smoker wait for dealer put tobacco and paper
        shared.pusherMatches.wait()
        # up counter when smoker smoke
        shared.matchesCounter += 1
        # print actual number of smoker calls
        print(f"matches count -> {shared.matchesCounter}")
        make_cigarette("matches")
        smoke("matches")


def smoker_tobacco(shared):
    """
    Function represented smoking of smoker with tobacco
    :param shared: class contain all steering elements
    :return: nothing
    """
    while True:
        sleep(randint(0, 10) / 100)
        # smoker wait for dealer put matches and paper
        shared.pusherTobacco.wait()
        # up counter when smoker smoke
        shared.tobaccoCounter += 1
        # print actual number of smoker calls
        print(f"tobacco count -> {shared.tobaccoCounter}")
        make_cigarette("tobacco")
        smoke("tobacco")


def smoker_paper(shared):
    """
    Function represented smoking of smoker with paper
    :param shared: class contain all steering elements
    :return: nothing
    """
    while True:
        sleep(randint(0, 10) / 100)
        # smoker wait for dealer put matches and tobacco
        shared.pusherPaper.wait()
        # up counter when smoker smoke
        shared.matchesCounter += 1
        # print actual number of smoker calls
        print(f"paper count -> {shared.matchesCounter}")
        make_cigarette("paper")
        smoke("paper")


def agent_t_p(shared):
    """
    Signalizing can push tobacco and paper on table for pusher
    :param shared: class contain all steering elements
    :return: nothing
    """
    while True:
        sleep(randint(0, 10) / 100)
        print("push -> tobacco, paper \nrun -> matches")
        shared.tobacco.signal()
        shared.paper.signal()


def agent_p_m(shared):
    """
    Signalizing can push matches and paper on table for pusher
    :param shared: class contain all steering elements
    :return: nothing
    """
    while True:
        sleep(randint(0, 10) / 100)
        print("push -> paper, matches \nrun -> tobacco")
        shared.paper.signal()
        shared.matches.signal()


def agent_t_m(shared):
    """
    Signalizing can push tobacco and matches on table for pusher
    :param shared: class contain all steering elements
    :return: nothing
    """
    while True:
        sleep(randint(0, 10) / 100)
        print("push -> tobacco, match \nrun -> paper")
        shared.tobacco.signal()
        shared.matches.signal()


def pusher_matches(shared):
    """
    Pusher for push tobacco or paper
    :param shared: class contain all steering elements
    :return: nothing
    """
    while True:
        shared.matches.wait()
        shared.mutex.lock()
        if shared.isTobacco:
            shared.isTobacco -= 1
            shared.pusherPaper.signal()
        elif shared.isPaper:
            shared.isPaper -= 1
            shared.pusherTobacco.signal()
        else:
            shared.isMatches += 1
        shared.mutex.unlock()


def pusher_paper(shared):
    """
    Pusher for push tobacco or matches
    :param shared: class contain all steering elements
    :return: nothing
    """
    while True:
        shared.paper.wait()
        shared.mutex.lock()
        if shared.isMatches:
            shared.isMatches -= 1
            shared.pusherTobacco.signal()
        elif shared.isTobacco:
            shared.isTobacco -= 1
            shared.pusherMatches.signal()
        else:
            shared.isPaper += 1
        shared.mutex.unlock()


def pusher_tobacco(shared):
    """
    Pusher for push paper or matches
    :param shared: class contain all steering elements
    :return: nothing
    """
    while True:
        shared.tobacco.wait()
        shared.mutex.lock()
        if shared.isPaper:
            shared.isPaper -= 1
            shared.pusherMatches.signal()
        elif shared.isMatches:
            shared.isMatches -= 1
            shared.pusherPaper.signal()
        else:
            shared.isTobacco += 1
        shared.mutex.unlock()


if __name__ == "__main__":
    shared = Shared()

    smokers = [Thread(smoker_matches, shared), Thread(smoker_tobacco, shared), Thread(smoker_paper, shared)]
    pushers = [Thread(pusher_matches, shared), Thread(pusher_paper, shared), Thread(pusher_tobacco, shared)]
    agents = [Thread(agent_t_p, shared), Thread(agent_p_m, shared), Thread(agent_t_m, shared)]

    for t in smokers + pushers + agents:
        t.join()
