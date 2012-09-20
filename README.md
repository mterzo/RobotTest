RobotTest
=========
This is some sample code to test candidates on their ability to look at code, 
devise a test plan, and create tests. The daemon should start up correctly and 
the provided example test should pass, but otherwise we make no promises. This 
code is full of bugs.

What is this:
=============
This is some sample code to test canidates on their ability to look at code
and devise a test plan and create tests.  

Installation:
=============
Requires Python.  I've tested with python 2.7.3, on windows and linux.  I've also tested python 2.4.  To use Robot you will need python 2.7.3

Download 
   - Python: http://python.org/download/
   - RobotFramework: https://code.google.com/p/robotframework/
   - (optional) Ride: https://github.com/robotframework/RIDE/downloads
   - (optional) wxPython (for Ride): http://wxpython.org/download.php#stable

Usage:
=============
To start the daemon

> python src/robottest.py

Basic Spec:
===========
So this Dameon is to open up a port 2059 and listen to incomming connection. 
At which point it has a basic telnet style user/pass prompt.  You are allowed 3
attempts to enter correct user/name password.  Usernames and password are case 
sensitive.  At which point there are some basic commands available.

And that's all you get.  This is white box testing so have a look at the code
for the rest of what can be done.

To get you started with Robot:
=========
The initial robot login test case for 1 user.  tests/RobotTest.txt

Enjoy!
