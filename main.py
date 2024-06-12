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
