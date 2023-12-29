# Moore Machine in Python

This project implements a Moore Machine in Python. A Moore Machine is a finite state machine where the outputs depend only on the current state.

### So far, the Moore Machine works by taking the input and increasing it by 1. The completed methods are pwl, input passing, and plotting. TODO: Clock, Bus, Actual Machine 

## Table of Contents
- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Introduction
A Moore Machine is a type of finite state machine (FSM) named after the American engineer and computer scientist Edward F. Moore. In a Moore Machine, the outputs are associated with states rather than transitions. This means that the output of the system is determined solely by the current state, not by the input or the transition taken.

Here are the key characteristics of a Moore Machine:

    States: The system can be in one of a finite number of states.
    Inputs: External inputs can trigger transitions between states.
    Outputs: Each state is associated with a specific output.

The transition between states in a Moore Machine is based solely on the input, and the output is a function of the current state. This makes Moore Machines particularly useful for modeling systems where the output depends on the current state of the system.

## Installation
In order to install this project, download the zip file from above and extract it to your local destination. 

## Usage

The following code specifies a sample way to create and run the Moore Machine. It is also present in the file main.py.
It consists of 2 machines m1 and m2. The input is received from the text file and the final output is stored in the object o. 
The input can be from any type of file that has the extension .txt, .csv, and .xslx. 

Feature: Each of the specified file types can have a header line which can contain anything, the program will automatically skip it / ignore it.

        For txt files, the format should be as follows: 
            <time> <input>
            <time> <input>
            ...
            time should be convertible to float.
            input should be convertible to integer.
            
        For csv files, the format should be as follows:
            It assumes that the newline was set to "" while creating the file.
            A sample creation in python:

```python
        import csv
        with open("Test.csv", "w", newline='') as file:
            csw=csv.writer(file)
            for i in range(5):
            csw.writerow([i+0.1,i+1])
```
                
            Input format that is expected in the file as follows:            
            <time>,<input>
            <time>,<input>
            ...
            time should be convertible to float.
            input should be convertible to integer.

        For xlsx files, the format should be as follows:
        Input format is expected in the file as follows:    
            Column:  A         B
                    <time>   <input>
                    <time>   <input>
                    <time>   <input>
                    ...
            time should be convertible to a float.
            input should be convertible to integer.

Look at Tests\\Test.txt, Tests\\Test.csv, Tests\\Tests.xslx for more information.

A sample txt file, csv file, and xslx file are shown below (Note headers are not required) :

    Txt File: 
            Time Input
            0.1 1
            1.1 2
            2.1 3
            3.1 4
            4.1 5
    CSV File:
            time,inputs
            0.1,1
            1.1,2
            2.1,3
            3.1,4
            4.1,5
    XSLX File:
    Column: A    B
            Time Input
            0.1	 1
            1.1	 2
            2.1	 3
            3.1	 4
            4.1	 5

```python
from blocks import Manager, Clock

manager = Manager()
i = manager.addInput("Tests\\Test.txt", "input")
m1 = manager.addMachine(Clock(), 1, 1, True, "m1")
m2 = manager.addMachine(Clock(), 1, 1, True, "m2")
o = manager.addOutput("output")

#Making all the connections
m1 <= i #i is an input to m1.
m2 <= m1 #m1's output is an input to m2.
o <= m2 #m2's output is an input to o.

#Running all the blocks.
manager.run(until = 40)
```

## License
It is an open-source project. 
