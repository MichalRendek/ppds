"""
Copyright 2022 Michal Rendek
Licenced to MIT https://spdx.ogr/licenses/MIT.html

This module implements the solution for generators and scheduler
"""

import random


def task1():
    """
    Task 1 which increase number
    """
    count = 1
    while True:
        count += 1
        # control print
        print(f'Task1 {count}')
        yield


def task2():
    """
    Task 2 which print random number from 1 to 99
    """
    while True:
        num = random.randint(1, 100)
        # control print
        print(f'Task2 {num}')
        yield


def task3():
    """
    Task 3 which increase or decrease number base on random number
    """
    count = 1
    while True:
        num = random.randint(0, 1)
        if num:
            count += 1
        else:
            count -= 1
        # control print
        print(f'Task3 {count}')
        yield


class Scheduler:
    """
    Class representative Scheduler for tasks
    """
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        """
        Function for add task to scheduler
        :param task: task for run
        """
        self.tasks.append(task)

    def run(self, iterations):
        """
        Function for run scheduler and tasks inside
        :param iterations: number of rerun tasks
        """
        for i in range(1, iterations):
            # random select task from array
            task_num = random.randint(0, len(self.tasks) - 1)
            # rerun task
            next(self.tasks[task_num])


if __name__ == "__main__":
    # create scheduler
    scheduler = Scheduler()

    # add tasks to scheduler
    scheduler.add_task(task1())
    scheduler.add_task(task2())
    scheduler.add_task(task3())

    # run scheduler with number of iterations (30 in this implementation)
    scheduler.run(30)
