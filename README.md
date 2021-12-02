Hello!

The files contained within this GitHub repository act to function as a ticket viewer for Zendesk.
Zendesk provides software related to customer service, sales and various other communications related
aspects of a company. 

Each account created with Zendesk recieves tickets. These tickets display requests, complaints, and 
questions made by customers may have made. This application acts as a viewer for these tickets.
It communicates directly with Zendesk's RESTful API and gets the tickets displayed in your account.

INSTALLATION INSTRUCTIONS

1. Install Python.

This program is written in python. This means that you will have to install Python to use it. Luckily,
this is pretty easy to do, see installation intructions here: https://www.ics.uci.edu/~pattis/common/handouts/pythoneclipsejava/python.html


2. Copy the files to your computer.

Copy funcs.py, main.py and ticket.py to any folder you wish. That's it.


3. Make sure pip is installed.

If you just installed Python for Windows, you should have it already. If you're using Linux, then 
follow these instructions: https://packaging.python.org/guides/installing-using-linux-tools/.
You can double check to see if you have pip anyways using these commands

Unix/macOS:

    python3 -m pip --version

Windows:

    py -m pip --version


4. Installing Python libraries

This program usses some of Python's very helpful libraries. Using the command line, navigate to the 
folder which contains these Python files. Then, type the following:

Windows:

    py -m pip install tabulate
    py -m pip install requests

Unix/macOS:

    python3 -m pip install tabulate
    python3 -m pip install requests


5. Use it!

Navigate to the folder you've pasted main.py, funcs.py and ticket.py to from the command line.
Then you run can run main.py as follows:

Windows:

    python main.py

Unix/macOS:

    python3 main.py

Should be good to go! If this dosen't work out, feel free to reach out to me at lemurwebsites@gmail.com.

Enjoy!