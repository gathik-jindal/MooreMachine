"""
This class is used for creating all the blocks.
It requires you to download simpy which can be done by

pip install simpy

@author: Abhirath, Aryan, Gathik
@date: 27/12/2023
@version: 1.0
"""
from blocks import Manager

if __name__ == "__main__":

    #Creating a manager class and adding all the blocks to it.
    manager = Manager()
    clk=manager.addClock()
    i = manager.addInput("Tests\\Test.txt", "input")
    m1 = manager.addMachine(clk, 1, 1, True, "m1")
    m2 = manager.addMachine(clk, 1, 1, True, "m2")
    o = manager.addOutput("output")

    #Making all the connections
    m1 <= i
    m2 <= m1
    o <= m2

    #Running all the blocks.
    manager.run(until = 40)
