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
