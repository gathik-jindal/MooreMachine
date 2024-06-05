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

The transition between states in a Moore Machine is based solely on the input, and the output is a function of the current state. This makes Moore Machines particularly useful for modelling systems where the output depends on the current state of the system.

## Installation

In order to install this project, download the zip file from above and extract it to your local destination.

## Usage

### Inputs
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

### Starting Simulation

'''python
from pydig import pydig as pd

'''

### Creation of objects

#### Moore, ........

#### Moore, ........

#### Moore, ........

#### Building Blocks

### Making Connections

### Generating CSV

### Run


The following code specifies a sample way to create and run the Moore Machine. It is also present in the file main.py.
It consists of 2 machines m1 and m2. The input is received from the text file and the final output is stored in the object o.


```python
"""
This is a sample code of how a PWM can be simulated using this simulator

The PWM we have designed takes 4 bits of input from a user created file (In our case: "Test\\PWM.csv")
The first 2 bits (LSB) give the onTime for the PWM (Durition of each "High" in the required clock)
The second 2 bits (MSB) give the Time Period of the PWM (The 2 bit number + 1 is taken as the time period of the required clock)

@author: Abhirath, Aryan, Gathik
@date: 4/12/2023
@version: 1.6
"""

import pydig

# Functions with the required logics


def n(a):

    # This is the logic of a single input not gate
    return (~a & 0b1)


def nsl(ps, i):

    # This is the Next State Logic for the PWM

    a = (ps >> 1) & 1
    b = (ps >> 0) & 1

    d = (n(a) & b & n(i)) | (a & n(b) & n(i))
    e = (n(b) & n(i))

    return d << 1 | e


def ol(ps):

    # This is the output logic for the PWM
    return ps


# Actual simulation begins from here.

# Setup a simulator object to begin simulation
pysim = pydig.pydig(name="PWM")

# Creating an source object and connecting it to the required file
PWM_Path = "Tests\\PWM.csv"
PWM_Input = pysim.source(filePath=PWM_Path, plot=False, blockID="PWM Input")

# Creating the clock
clk = pysim.clock(plot=False, blockID="clk", timePeriod=1, onTime=0.5)

# Creating the moore machine
mod4Counter = pysim.moore(maxOutSize=2, plot=True, blockID="Mod 4 Counter", startingState=0)
mod4Counter.nsl = nsl
mod4Counter.ol = ol

# Creating the comparators
syncResetComparator = pysim.combinational(maxOutSize=1, plot=False, blockID="Sync Reset Comparator", func=lambda x: int((x & 3) == (x >> 2)), delay=0)
outputComparator = pysim.combinational(maxOutSize=1, plot=False, blockID="Output Comparator", func=lambda x: int((x & 3) > (x >> 2)), delay=0)

# Final output object
finalOutput = pysim.output(plot=True, blockID="PWM Output")

# Creating the connections

syncResetComparator.output() > mod4Counter.input()
clk.output() > mod4Counter.clock()

PWM_Input.output(0, 2) > outputComparator.input()
mod4Counter.output() > outputComparator.input()

PWM_Input.output(2, 4) > syncResetComparator.input()
mod4Counter.output() > syncResetComparator.input()

outputComparator.output() > finalOutput.input()

# This prepares a csv file where the simulation can be recorded and stored for later use.
pysim.generateCSV()

# Runs the simulation and plots the results
pysim.run(until=40)
```
