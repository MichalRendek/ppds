# Exercise seven

## Generators and scheduler
### Description 
Write an application that will use N (N> 2) coprograms (using advanced generators) and use your own scheduler to rotate 
them. Do not use program code from the recommended literature for the solution.
### Solution 
#### Code
In my case, I use base scheduler generate random number and select coprogram by it.

```python
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
```

Then in main add task / coprograms

```python
# create scheduler
scheduler = Scheduler()

# add tasks to scheduler
scheduler.add_task(task1())
scheduler.add_task(task2())
scheduler.add_task(task3())

# run scheduler with number of iterations (30 in this implementation)
scheduler.run(30)
```

Tasks are creat as simple functions return by `yield` for go out from function and on call with `next` go back in.

```python
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
```

Simple but right.
