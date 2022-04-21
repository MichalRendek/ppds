"""
Copyright 2022 Michal Rendek
Licenced to MIT https://spdx.ogr/licenses/MIT.html

This module implements the solution for generators and scheduler
"""
import numpy as np
import time


class Arrays:
    """
    Class for store and filling arrays
    """
    def __init__(self):
        self.arrays = []

    def fill_arrays(self, num):
        """
        Function for filling and create new array
        :param num: number of arrays
        """
        for i in range(num):
            self.arrays.append(np.random.randint(1, 26, 100))


def find_in_array(num, arrays, array_num):
    """
    Function for find number in array, if is number find print position of this number
    :param num: finding number
    :param arrays: class store arrays
    :param array_num: number of working array
    """
    for i in range(len(arrays.arrays[array_num])):
        if arrays.arrays[array_num][i] == num:
            print(f'number {num} is on position {i+1} in {array_num + 1}. array')


if __name__ == "__main__":
    # number of create arrays
    arrays_number = 3000
    arrays = Arrays()
    # fill number of arrays
    arrays.fill_arrays(arrays_number)
    start_time = time.perf_counter()
    # search specific number (7 here) in arrays
    for i in range(arrays_number):
        find_in_array(7, arrays, i)
    elapsed = time.perf_counter() - start_time
    # print final time
    print(f"\nTotal elapsed time: {elapsed:.10f}")
