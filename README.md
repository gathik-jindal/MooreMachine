# <ins>Moore Machine in Python</ins>

This project implements a Moore Machine in Python. A Moore Machine is a finite state machine where the outputs depend only on the current state.

## <ins>Table of Contents</ins>

- [Introduction](#introduction)
- [Installation](#installation)
- [Libraries](#libraries)
- [Usage](#usage)
- [Different Building Blocks](#different-building-blocks)
- [Sample Code](#sample-code)
- [Elaborations and Explanations](#elaborations-and-explanations)

## <ins>Introduction</ins>

A Moore Machine is a type of finite state machine (FSM) named after the American engineer and computer scientist Edward F. Moore. In a Moore Machine, the outputs are associated with states rather than transitions. This means that the output of the system is determined solely by the current state, not by the input or the transition taken.

Here are the key characteristics of a Moore Machine:

    States: The system can be in one of a finite number of states.
    Inputs: External inputs can trigger transitions between states.
    Outputs: Each state is associated with a specific output.

The transition between states in a Moore Machine is based solely on the input, and the output is a function of the current state. This makes Moore Machines particularly useful for modelling systems where the output depends on the current state of the system.

## <ins>Installation</ins>

In order to install this project, download the zip file from above and extract it to your local destination.

## <ins>Libraries</ins>

The following libraries are required to be installed : 
    
    1) simpy
    2) matplotlib
    3) openxl (for reading excel files)

You can install them by running the following commands : 
    
    1) pip install simpy
    2) pip install matplotlib
    3) pip install openxl

## <ins>Usage</ins>

### <ins>Starting the Simulation</ins>

To start off, we need to create a simulation object, that handles the creation of objects.
This can be done by the following code:

```python
import pydig

variable_name_for_this_simulation_object = pydig.pydig(name="<Name of This simulation (used while generating output csv files)>")
# we will use "pysim" as a variable name for this object in the following examples.
```

### <ins>Creation of objects</ins>

The following objects can be created:

    1. Input Block
    2. Moore Machine
    3. Combinational Block
    4. Clock
    5. Output Block

#### <ins>Input Block</ins>

The input block is designed to handle file inputs in various formats, including csv, txt, and xlsx. It reads the content of the file and processes it for further use in the application.

Supported File Formats
csv (Comma-Separated Values): A plain text file that uses commas to separate values.
txt (Text): A plain text file that contains unformatted text.
xlsx (Excel Spreadsheet): A Microsoft Excel file format that contains data in a tabular form with rows and columns.

Refer to [Inputs From Files](#inputs-from-files) for more information on the file format. 

```python
variable_name = pysim.source(filepath = "<filePath>", plot = <True/False>, blockID = "<Name of the block>")
``` 
Parameters :

    1) 'filepath' (str): The path to the input file. This should be a string indicating the location of the file on the local filesystem. The file can be in CSV, TXT, or XLSX format.
    2) 'plot' (bool): A boolean flag that indicates whether the data should be visualized (plotted) after being read. If True, the function will generate a plot of the data. If False, no plot will be generated. (default is False)
    3) 'blockID' (str): A unique identifier for the input block. This string is used to reference and manage the block. If the id is not unique, then a new id would be created and the user would be notified.

The above command returns an Input object.
The methods available for the user are at [Input Block Methods](#input-block-methods).

#### <ins>Moore Machine</ins>

The Moore Machine is created by the following code:

```python
def _nsl(presentState, input):
    # some function
    return nextState
def _ol(presentState):
    # some function
    return output

Variable_name = pysim.moore(plot = <True/False>, blockID = "<Name of the block>", nsl = _nsl, ol = _ol)
```

The parameters that it accepts are listed below in order:

    1) 'maxOutSize' (int): the maximum number of output wires
    2) 'plot' (bool): boolean value whether to plot this moore machine or not
    3) 'blockID' (str): the id of this machine. If None, then new unique ID is given.  
    4) 'nsl' (function): next state logic function, this accepts two arguments, the first is the input and the second is the present state.
    5) 'ol' (function): output logic function
    6) 'startingState' (int): the starting value for all the wires excpet the output of the moore machine, the values should be less than 2^maxOutSize.

The above command returns a Moore Machine object.
The following methods are available for the user at [Moore Machine Methods](#moore-machine-methods).

#### <ins>Combinational Block</ins>

This Block is to be used when needed insert a combinational logic in between.
The Combinational Block is created by the following code:

```python
def _function(input):
    # some function
    return output

Variable_name = pysim.combinational(plot = <True/False>, blockID = "<Name of the block>", function = _function)
```

The parameters that it accepts are listed below in order:

    1) 'maxOutSize' (int): the maximum number of parallel output wires
    2) 'plot' (boolean): boolean value whether to plot this moore machine or not
    3) 'blockID' (str): the id of this machine. If None, then new unique ID is given.
    4) 'function' (function): inner gate logic
    5) 'delay' (float): the time delay for this object
    6) 'initialValue' (int): The initial output value given by this block at t = 0 while running

The above command creates a Combinational Block object.
The following methods are available for the user at [Combinational Block Methods](#combinational-block-methods).

#### <ins>Clock Block</ins>

The Clock Block is created by the following code:

```python
Variable_name = pysim.clock(plot = <True/False>, blockID = "<Name of the block>", timePeriod = <float>, onTime = <float>, initialValue = <int>)
```

The parameters that it accepts are listed below in order:

    1) plot (boolean): boolean value whether to plot this clock or not
    2) blockID (str): the id of this clock. If None, then new unique ID is given.  
    3) timePeriod (float): the time period of this clock.
    4) onTime (float): the amount of time in each cycle that the clock shows high (1).
    5) initialValue (int): the initial value of the clock (default is 0)

NOTE: This block has no input connection and only has an output connection.

#### <ins>Output Block</ins>

The Output Block is created by the following code:

```python
Variable_name = pysim.output(plot = <True/False>, blockID = "<Name of the block>")
```

The parameters that it accepts are listed below in order:

    1) plot (boolean): boolean value whether to plot this output source or not
    2) blockID (str): the id of this input block. If None, then new unique ID is given.

NOTE: This block has only input connections and no output connections.

#### <ins>Building Blocks</ins>

There are numerous pre-built objects that can directly be used for more complex simulations
To read more about it click on [Different Building Blocks](different-building-blocks)

### <ins>Making Connections</ins>

There are 2 ways to make connections between Blocks. Both these are identical in function and properties. The user can use the method they find comfortable.

```python
#Method 1
Block1.output(a, b) > Block2.input()
    
#Method 2
Block2.input() <= Block1.output(a,b)
```
In the above code we have taken output bits `a`(inclusive) to `b`(exclusive) of Block1 and connected it to the input of Block2.

NOTE:

1) In this example we have to make sure that Block2 can accept input connections and Block1 has valid output lines. 

2) By "bits `a` to `b`" we mean the first bit connected is the `a`th bit from the LSB and the last bit connected will be `b - 1`th bit from the LSB starting our numbering from 0.
For example: if the output value is `11001` and we do `.output(1,4)` we connect the middle 3 bits holding `100`.

3) If we just write `.output()` it will automatically connect all bits. If we write `.output(a)` It will connect all bits from `a`(inclusive) till the end of the value. 

4) We can do multiple connections in a row like:

```python
Block1 > Block2 > Block3 .......
```
But the output connections using this method will include all output bits being connected to the next block.

5) If we wish to connect a clock to the input of a Moore machine we use `Moore.input()` and If we wish to connect it to the registers of the Moore Machine then we use `Moore.clock()`

```python    
Clock1.output() > Moore.input()
Clock2.output() > Moore.clock()
```

To know about more features one can use to make connections go to: [More on types of connections](#More-on-types-of-connections)

### <ins>Generating the CSV File</ins>

In order to generate a csv file for a simulation we have to write the line `pysim.generateCSV()` before running the simulation. This will create a csv file having the name of the simulation object and will hold the values of all the blocks present in that simulation.

### <ins>Running and Plotting the simulation</ins>

To run the simulation we need to write `pysim.run(until = <duration of simulation>)`. This line

## <ins>Different Building Blocks</ins>

### <ins>BitCounters</ins>

This file contains 1 - 4 bit counters that take an enable line as input and 
the output is the actual output of the counter as well as the terminal count
of the counter. 
When the enable line is high, the counter starts counting and when the enable line
is low, the counter is frozen. 
The terminal count of the counter is high only when the counter's output is the max value of the counter.

#### <ins>Enabled1BitCounterWithTC</ins>

This is an enabled 1 bit counter. The output of the counter is either 0 or 1. When the output of the counter is 1, the terminal count of the counter is high.

```python
from BuildingBlocks.BitCounters import Enabled1BitCounterWithTC as Counter

variable_name = Counter(pydig = pysim, enable = inputObject, clock = clockObject, plot = <True/False>)
```

The parameters that it accepts are listed below in order:
        1) pydig : a pydig object that you want to add this counter to.
        2) enable : a HasOutputConnection object (an Input object, a Machine object, or a Combinational object).
        3) clock : a clock object
        4) plot : a boolean value whether to plot this object or not (default is True)

The above command creates a Combinational Block object.
The following methods are available for the user at [Combinational Block Methods](#combinational-block-methods).

#### <ins>Enabled2BitCounterWithTC</ins>

This is an enabled 2 bit counter. The output of the counter is 0-3. When the output of the counter is 3, the terminal count of the counter is high.

```python
from BuildingBlocks.BitCounters import Enabled2BitCounterWithTC as Counter

variable_name = Counter(pydig = pysim, enable = inputObject, clock = clockObject, plot = <True/False>)
```

The parameters that it accepts are listed below in order:
        1) pydig : a pydig object that you want to add this counter to.
        2) enable : a HasOutputConnection object (an Input object, a Machine object, or a Combinational object).
        3) clock : a clock object
        4) plot : a boolean value whether to plot this object or not (default is True)

The above command creates a Combinational Block object.
The following methods are available for the user at [Combinational Block Methods](#combinational-block-methods).

#### <ins>Enabled3BitCounterWithTC</ins>

This is an enabled 3 bit counter. The output of the counter is 0-7. When the output of the counter is 7, the terminal count of the counter is high.

```python
from BuildingBlocks.BitCounters import Enabled3BitCounterWithTC as Counter

variable_name = Counter(pydig = pysim, enable = inputObject, clock = clockObject, plot = <True/False>)
```

The parameters that it accepts are listed below in order:
        1) pydig : a pydig object that you want to add this counter to.
        2) enable : a HasOutputConnection object (an Input object, a Machine object, or a Combinational object).
        3) clock : a clock object
        4) plot : a boolean value whether to plot this object or not (default is True)

The above command creates a Combinational Block object.
The following methods are available for the user at [Combinational Block Methods](#combinational-block-methods).

#### <ins>Enabled4BitCounterWithTC</ins>

This is an enabled 4 bit counter. The output of the counter is 0-15. When the output of the counter is 15, the terminal count of the counter is high.

```python
from BuildingBlocks.BitCounters import Enabled4BitCounterWithTC as Counter

variable_name = Counter(pydig = pysim, enable = inputObject, clock = clockObject, plot = <True/False>)
```

The parameters that it accepts are listed below in order:
        1) pydig : a pydig object that you want to add this counter to.
        2) enable : a HasOutputConnection object (an Input object, a Machine object, or a Combinational object).
        3) clock : a clock object
        4) plot : a boolean value whether to plot this object or not (default is True)

The above command creates a Combinational Block object.
The following methods are available for the user at [Combinational Block Methods](#combinational-block-methods).

### <ins>FreezeCounter</ins>

A freeze counter is a type of counter in which if the input is high,
the counter "freezes" or, in other terms, stays at the same value until
the input becomes low again.

```python
from BuildingBlocks.FreezeCounter import FreezeCounter as Counter

variable_name = Counter(pydig = pysim, modValue: int, freeze = inputObject, clock = clockObject, plot = <True/False>)
```

The parameters that it accepts are listed below in order:
        1) pydig : pydig object
        2) modValue : the maximum value of the counter
        3) freeze : the freeze signal
        4) clock : the clock signal
        5) plot : boolean value whether to plot this moore machine or not (default is True)

The above command creates a Combinational Block object.
The following methods are available for the user at [Combinational Block Methods](#combinational-block-methods).

### <ins>SynchronousCounter</ins>

The Synchronous Counter is a counter that increments its value only when
the clock signal is high and the counter resets when the reset signal is high.
The counter is a modulo counter, i.e., it resets to zero when it reaches
the maximum value.

```python
from BuildingBlocks.SynchronousCounter import SynchronousCounter as Counter

variable_name = Counter(pydig = pysim, modValue = <int>, syncReset = inputObject, clock = clockObject, plot = <True/False>)
```

The parameters that it accepts are listed below in order:
        1) pydig : pydig object
        2) modValue : the maximum value of the counter
        3) syncReset : the synchronous reset signal
        4) clock : the clock signal
        5) plot : boolean value whether to plot this moore machine or not (default is True)

The above command creates a Combinational Block object.
The following methods are available for the user at [Combinational Block Methods](#combinational-block-methods).

### <ins>SynchronousCounterWithPeriod</ins>

The Synchronous Counter is a counter that increments its value only when
the clock signal is high. The counter resets when the value of the counter reaches "period"
The counter is implemented using a Moore machine. The Moore machine has the next state logic as the increment function and the output logic as the identity function. The counter is implemented using the Combinational block.

```python
from BuildingBlocks.SynchronousCounterWithPeriod import SynchronousCounterWithPeriod as Counter

variable_name = Counter(pydig = pysim, modValue = <int>, period = inputObject, clock = clockObject, plot = <True/False>)
```

The parameters that it accepts are listed below in order:
        1) pydig : pydig object
        2) modValue : the maximum value of the counter
        3) period : the synchronous reset signal
        4) clock : the clock signal
        5) plot : boolean value whether to plot this moore machine or not (default is True)

The above command creates a Combinational Block object.
The following methods are available for the user at [Combinational Block Methods](#combinational-block-methods).

### <ins>Latches</ins>

Latches are fundamental building blocks in digital design used to store a single bit of data. They are level-sensitive devices, meaning their output state depends on the input level rather than the edge of the input signal. Latches are classified into two main types: SR (Set-Reset) latches and D (Data or Delay) latches.

SR Latch: Consists of two inputs, Set (S) and Reset (R), which control the state of the latch. When S is high, the latch is set, and when R is high, the latch is reset.

D Latch: Simplifies the SR latch by eliminating the possibility of invalid states. It has a single input, D, and a clock signal that determines when the input data is sampled and transferred to the output.

#### <ins>SRLatch</ins>

```python
from BuildingBlocks.Latches import SRLatch as Latch

variable_name = Latch(pydig = pysim, SR = inputObject, clock = clockObject, plot = <True/False>)
```

The parameters that it accepts are listed below in order:
        1) pydig : a pydig object that you want to add this counter to.
        2) SR : a HasOutputConnection object (an Input object, a Machine object, or a Combinational object).
        3) clock : a clock object
        4) plot : a boolean value whether to plot this object or not (default is True)

The above command creates a Combinational Block object.
The following methods are available for the user at [Combinational Block Methods](#combinational-block-methods).

#### <ins>DLatch</ins>

```python
from BuildingBlocks.Latches import DLatch as Latch

variable_name = Latch(pydig = pysim, D = inputObject, clock = clockObject, plot = <True/False>)
```

The parameters that it accepts are listed below in order:
        1) pydig : a pydig object that you want to add this counter to.
        2) D : a HasOutputConnection object (an Input object, a Machine object, or a Combinational object).
        3) clock : a clock object
        4) plot : a boolean value whether to plot this object or not (default is True)

The above command creates a Combinational Block object.
The following methods are available for the user at [Combinational Block Methods](#combinational-block-methods).

## <ins>Sample Code</ins>

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

# <ins>Elaborations and Explanations</ins>

## <ins>Inputs From Files</ins>
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


## <ins>More on types of connections</ins>

The simulator can handle different types of connections.

### <ins>Single Out vs Multiple Out:</ins>

The simulator can internally handle both of these types of connections. If a block, say `Block0`, has only one connection going out. It is treated as a Single-Output connection. If we have a block, say `Block1`, having multiple connections going out then it is treated as a Multiple-Output connection. Both are valid and the range of bits we select need not be the same nor be mutually exclusive. (a,b), (c,d) and (e,f) can be any range of values and the simulator can handle it accordingly. 


```python
Block0.output(a,b) > Block1.input()

Block1.output(c,d) > Block2.input()
Block1.output(e,f) > Block3.input()
```

### <ins>Single In vs Multiple In:</ins>


<<<<<<<<<<<<<<>>>>>>>>>>>>>>

```python
Block0.output(a,b) > Block1.input()

Block1.output(c,d) > Block2.input()
Block0.output(e,f) > Block2.input()
```

## <ins>Input Block Methods</ins>

The following methods are available for the user : 
    variable_name.output(left = 0, right = None)
        1) Refer to [Making Connections](#Making Connections) for more information on making connections

## <ins>Moore Machine Methods</ins>

The following methods are available for the user :
    
    1) `.isConnected()` (@return bool): return true if all the ports of the machine are connected.
    2) `.clock()` (@return object): return the object itself.
    3) `.input()` (@return object): return the object itself.
    4) `.getScopeDump()` (@return dict): return a dictionary of all the values along with a label.

## <ins>Combinational Block Methods</ins>

The following methods are available for the user :

    1) `.isConnected()` (@return bool): return true if all the ports of the machine are connected.