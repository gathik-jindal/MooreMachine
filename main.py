"""
This class is used for creating all the blocks.
It requires you to download simpy which can be done by

pip install simpy

@author: Abhirath, Aryan, Gathik
@date: 27/12/2023
@version: 1.0
"""

from blocks import pydig as pd

def NSL1(ps, i):
    return (i ^ ps)

def NSL2(ps, i):
    return (i | ps)

def OL1(ps):
    return (ps + 2) % 4

def OL2(ps):
    return (ps & 5)

if __name__ == "__main__":

    # Creating a pydig class and adding all the blocks to it.
    pydig = pd()
    clk = pydig.clock(blockID= "clk1", timePeriod = 1.4, onTime = 0.7)
    i = pydig.source("Tests\\Test.txt", "input")
    m1 = pydig.moore(plot = True, blockID = "m1")
    m2 = pydig.moore(plot = True, blockID = "m2")
    o = pydig.output(blockID = "out")

    print(clk, i, m1, m2, o, sep = "\n")

    # Assigning the different components
    m1.nsl = NSL1
    m1.ol = OL1
    m2.nsl = NSL2
    m2.ol = OL2
    
    # Making all the connections
    i.output() > m1.input()
    m1.output() > m2.input()
    m2.output() > o.input()
    clk.output() > m1.clock()
    clk.output() > m2.clock()
    # Creating dump
    pydig.dumpVars()

    # Running all the blocks.
    pydig.run(until = 21)
