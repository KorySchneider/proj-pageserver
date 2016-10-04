# README

### What is this?

This is a very (VERY) simple web server written in python. It only serves html and css files.

### Installation

To get this server up and running, execute the following commands:

    $ cd path/where/you/want/it
    $ git clone https://github.com/KorySchneider/proj-pageserver
    $ make

This will build/install the server and start it up on port 8000. Open up your browser and navigate to "localhost:8000/trivia.html" to make sure it is working. 

### Usage

To run the server, run the following command:

    $ python3 pageserver.py -p <port>

where `<port>` is a number between 1024 and 10000.

### Credit

Forked from Michal Young at https://github.com/UO-CIS-322/proj-pageserver for CIS 322: Intro to Software Engineering.
