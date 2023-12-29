# MooreMachine

Making a simple Moore Machine

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

The following code specifies a sample way to create and run the Moore Machine. It consists of 2 machines m1 and m2.
The input is received from the text file and the final output is stored in the object o. 

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
