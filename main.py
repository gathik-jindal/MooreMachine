"""
This class is used for creating all the blocks.
It requires you to download simpy which can be done by

pip install simpy

@author: Abhirath, Aryan, Gathik
@date: 27/12/2023
@version: 1.0
"""
from blocks import pydig as pd

def NSL1(i, ps):
    return 0

def NSL2(i, ps):
    return 0

def OL1(ps):
    return 0

def OL2(ps):
    return 0

if __name__ == "__main__":

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
    m1.clk = clk.output()
    m2.clk = clk.output()
    
    # Making all the connections
    i.output() > m1.input()
    m1.output() > m2.input()
    m2.output() > o.input()

    # Creating dump
    pydig.dumpVars()

    # Running all the blocks.
    pydig.run(until = 40)
