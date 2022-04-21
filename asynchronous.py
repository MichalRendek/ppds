"""
Copyright 2022 Michal Rendek
Licenced to MIT https://spdx.ogr/licenses/MIT.html

This module implements the solution for generators and scheduler
"""
import numpy as np
import time
import asyncio


class AsyncIterator:
    """
    Class representative own async iterator
    """
    def __init__(self, seq):
        self.iter = iter(seq)

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            return next(self.iter)
        except StopIteration:
            raise StopAsyncIteration


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


async def find_in_array(num, arrays, array_num, output):
    """
    Function for find number in array, if is number find print position of this number
    :param num: finding number
    :param arrays: class store arrays
    :param array_num: number of working array
    :param output: array for store results
    """
    async for i in AsyncIterator(range(len(arrays.arrays[array_num]))):
        if arrays.arrays[array_num][i] == num:
            # cause function is async, results store in output array
            output.append('number ' + str(num) + ' is on position ' + str(i+1) + ' in ' + str(array_num + 1) + '. array')


async def main():
    output = []
    # number of create arrays
    arrays_number = 3000
    arrays = Arrays()
    # fill number of arrays
    arrays.fill_arrays(arrays_number)
    start_time = time.perf_counter()
    # search specific number (7 here) in arrays in async mode
    await asyncio.gather(*[find_in_array(7, arrays, i, output) for i in range(arrays_number)])
    # print results
    for t in output:
        print(t)
    elapsed = time.perf_counter() - start_time
    # print final time
    print(f"\nTotal elapsed time: {elapsed:.10f}")

if __name__ == "__main__":
    asyncio.run(main())
