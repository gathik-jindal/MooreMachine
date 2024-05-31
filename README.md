# Moore Machine in Python

This project implements a Moore Machine in Python. A Moore Machine is a finite state machine where the outputs depend only on the current state.

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)

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

The inputs to the Moore Machine can be from files that have the extension .txt, .csv, or .xlsx.

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
                    ...
            time should be convertible to a float.
            input should be convertible to integer.

Look at Tests\\Test.txt, Tests\\Test.csv, Tests\\Tests.xlsx for more information.

A sample txt file, csv file, and xlsx file are shown below (Note headers are not required) :

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
    XLSX File:
    Column: A    B
            Time Input
            0.1  1
            1.1  2
            2.1  3
            3.1  4
            4.1  5

The following code specifies a sample way to create and run the Moore Machine. It is also present in the file main.py.
It consists of 2 machines m1 and m2. The input is received from the text file and the final output is stored in the object o.

```python
from blocks import pydig as pd

def NSL1(i, ps):
    return 0

def NSL2(i, ps):
    return 0

def OL1(ps):
    return 0

def OL2(ps):
    return 0

# Creating a pydig class and adding all the blocks to it.
pydig = pd()
clk = pydig.clock()
i = pydig.source("Tests\\Test.txt", "input")
m1 = pydig.moore(plot = True, blockID = "m1")
m2 = pydig.moore(plot = True, blockID = "m2")
o = pydig.output(blockID = "out")

print(i, m1, m2, o, sep = "\n")

# Assigning the different components
m1.nsl = NSL1
m1.ol = OL1
m2.nsl = NSL2
m2.ol = OL2

# Making all the connections
i.output() > m1.input()
m1.output() > m2.input()
m2.output() > o.input()
clk.output() > m1.clk()
clk.output() > m2.clk()

# Creating dump
pydig.dumpVars()

# Running all the blocks.
pydig.run(until = 40)

```
