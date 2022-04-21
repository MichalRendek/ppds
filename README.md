# Exercise eight

## Synchronous and asynchronous
### Description 
Write your own (any) single-threaded application in two versions: synchronous and asynchronous (using native routines). 
In the enclosed documentation, explain the purpose of the application and make a performance comparison of the 
synchronous and asynchronous versions. Remember to justify the results obtained (acceleration, deceleration, 
unchanged performance).
### Solution
#### Describe my app
I wrote an application that generates the set number of arrays and fills them with 100 values between 1 and 26. 
Subsequently, this application calls a function that passes the individual arrays and lists the position of the number 
7 in each array.
#### Code of synchronous app
Arrays are store in Arrays class.
```python
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
```

Then I call function in for loop. Each loop call function under another array. This function write position of number
seven.
```python
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

```

#### Code of asynchronous app
In first Array class.
```python
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
```

Next I create function main, which run all app. This function is async function. In this function are all `find_in_array` 
run as async with `asyncio.gather`.
```python
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
```

This function is run in main with `asyncio`.
```python
if __name__ == "__main__":
    asyncio.run(main())
```
Function `find_in_array` is async too and for inside is also async. For this I create async iterator.
```python
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
```
Iterator:
```python
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
```

#### Conclusion 
Time of sync method.  
`Total elapsed time: 1.7324590000`

Time of async method.  
`Total elapsed time: 0.6623509000`