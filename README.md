# Exercise one
## Description
Write program for increment cells of array to number one while all array cells not be one.
Make it in function running on two Threads.
Program must run in Python 3.10.1

## Solution 1
In this solution is in while in counting function full body covered in mutex lock. <br />
This fix of problem secures that thread do not be changed during counter incrementation and array cell incrementation. <br />
Here is still problem with overspet array length, but it is fixit with longer array than we ned. <br />
But well, it work corectly.

## Solution 2
In this solution mutex covered all while cycle. <br />
This is no good idea because program run slowly. <br />
It is because program use two thread bud all while cycle run in one thread. <br />
Pros of this solution is that array can be right lenght.
