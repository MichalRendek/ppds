# Exercise five

## Task 1 / the problem of smokers
### Description 
According to the lecture, implement a solution to the problem of smokers. In the case of a modification 
in which the agent is not waiting for signaling of resource allocation, solve the problem of 
favoring smokers and describe this solution in the documentation in an appropriate manner.
### Solution 
#### Code
In my solution is used pushers. Every pusher wait for agent who signalize that material can
be pushed on table. If on table is another material, not pushed from pusher, pusher signalize 
for smoker,he can run. It is implemented here:

>       shared.matches.wait()
>           shared.mutex.lock()
>           if shared.isTobacco:
>               shared.isTobacco -= 1
>               shared.pusherPaper.signal()
>           elif shared.isPaper:
>               shared.isPaper -= 1
>               shared.pusherTobacco.signal()
>           else:
>               shared.isMatches += 1
>           shared.mutex.unlock()

This is example for matches pusher. Same for another pushers.<br>
When on table is not material from another pushers, pusher push own material.
Everything run in never ending loop.

#### The problem of favoring smokers
In shared object are added counters for solution this problem. Every counter up when smoker 
smoked cigarette. 

>       self.tobaccoCounter = 0
>       self.matchesCounter = 0
>       self.paperCounter = 0

Counting is implementing in smoker.

>       sleep(randint(0, 10) / 100)
>       # smoker wait for dealer put tobacco and paper
>       shared.pusherMatches.wait()
>       # up counter when smoker smoke
>       shared.matchesCounter += 1
>       # print actual number of smoker calls
>       print(f"matches count -> {shared.matchesCounter}")
>       make_cigarette("matches")
>       smoke("matches")

##### Conclusion
Is no problem that one smoker is still signalized first. Real problem is that one is called
still second. Then he is called half times less.

![img.png](img.png)

In my solution to the problem, the call of smokers alternates evenly so that each one is first and once a second. This 
solution proves to be sufficient to solve the problem.