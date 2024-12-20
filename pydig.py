"""
This class is used for creating all the blocks.
It requires you to download simpy, matplotlib, openxl which can be done by

pip install simpy
pip install matplotlib
pip install openxl

@author Abhirath, Aryan, Gathik
@date 4/12/2023
@version 1.6
"""

import os
import sys

# directory reach
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from utilities import printErrorAndExit, checkType, dumpVars
from scope import Plotter
from blocks import *
from usableBlocks import *
from pwlSource import InputGenerator
import simpy


class pydig:
    """
    This class is used for adding your moore machines, input block, and output block.
    """

    def __init__(self, name="pydig"):
        """
        Creates a new simpy environment.
        It is a manager class for all blocks. 
        @param name : the name of this object (It will be used as the name of the output CSV file produced by this object). 
        """

        self.__uniqueIDlist = []
        self.__env = simpy.Environment()
        self.__components = []
        self.__count = 0
        self.__name = name
        self.__dump = False

    def __makeUniqueID(self, blockType):
        """
        Makes a unique block id given the type of the block.
        @param blockType : str object for the type of the block
        @return str : a unique id for the block
        """

        while (f"{blockType} {self.__count}" in self.__uniqueIDlist):
            self.__count += 1
        return f"{blockType} {self.__count}"

    def combinational(self, maxOutSize, plot=False, blockID=None, func=lambda x: x, delay=0, initialValue=0):
        """
        Adds a combinational block to this class. 
        @param maxOutSize : the maximum number of parallel output wires
        @param plot : boolean value whether to plot this moore machine or not
        @para blockID : the id of this machine. If None, then new unique ID is given.  
        @param function : inner gate logic
        @param delay : the time delay for this object
        @param initialValue : The initial output value given by this block at t = 0 while running
        @return Combinational : a combinational instance. 
        """

        checkType([(plot, bool), (maxOutSize, int)])
        self.__count += 1
        if (blockID == None):
            blockID = self.__makeUniqueID("Combi")
        elif blockID in self.__uniqueIDlist:
            id = self.__makeUniqueID(blockID)
            print(f"{blockID} is already used so changing to {id}")
            blockID = id

        self.__uniqueIDlist.append(blockID)
        temp = Combinational(func=func, env=self.__env, blockID=blockID, maxOutSize=maxOutSize, delay=delay, plot=plot, initialValue=initialValue)
        self.__components.append(temp)
        return temp

    def combinationalFromObject(self, combObj):
        """
        Adds a combinational block to this class given a combinational object already created.
        @param combObj : a Combinational block
        @return Combinational : the same combinational block
        """

        checkType([(combObj, Combinational)])

        if combObj.getBlockID() in self.__uniqueIDlist:
            id = self.__makeUniqueID(combObj.getBlockID())
            print(f"{combObj.getBlockID()} is already used so changing to {id}")
            combObj.setBlockID(id)

        self.__uniqueIDlist.append(combObj.getBlockID())
        self.__components.append(combObj)
        return combObj

    def moore(self, maxOutSize, plot=False, blockID=None, nsl=lambda ps, i: 0, ol=lambda ps: 0, startingState = 0, risingEdge = True, clock  = None, nsl_delay = 0.01, ol_delay = 0.01, register_delay = 0.01):
        """
        Adds a moore machine to this class. 
        @param maxOutSize : the maximum number of output wires
        @param plot : boolean value whether to plot this moore machine or not
        @para blockID : the id of this machine. If None, then new unique ID is given.  
        @param nsl : next state logic function
        @param ol : output logic function
        @param startingState : the starting state of the moore machine
        @param risingEdge : boolean value if the block works on rising edge or falling edge
        @param clock : the clock object for this moore machine
        @param nsl_delay : the delay in the next state logic
        @param ol_delay : the delay in the output logic
        @param register_delay : the delay in the register
        @return MooreMachine : the moore machine instance. 
        """
        checkType([(plot, bool), (startingState, int), (risingEdge, bool), (nsl_delay, (int, float)), (ol_delay, (int, float))])

        self.__count += 1
        if (blockID == None):
            blockID = self.__makeUniqueID("Moore")
        elif blockID in self.__uniqueIDlist:
            id = self.__makeUniqueID("Moore")
            print(f"{blockID} is already used so changing to {id}")
            blockID = id

        self.__uniqueIDlist.append(blockID)
        temp = MooreMachine(env=self.__env, maxOutSize=maxOutSize, nsl=nsl, ol=ol, plot=plot, blockID=blockID, startingState=startingState, clk = clock, posEdge = risingEdge, nsl_delay = nsl_delay, ol_delay = ol_delay, register_delay = register_delay)
        self.__components.append(temp)
        return temp

    def mealy(self, maxOutSize, plot=False, blockID=None, nsl=lambda ps, i: 0, ol=lambda ps: 0, startingState=0, risingEdge = True, clock = None, nsl_delay = 0.01, ol_delay = 0.01, register_delay = 0.01):
        """
        Adds a mealy machine to this class. 
        @param maxOutSize : the maximum number of output wires
        @param plot : boolean value whether to plot this moore machine or not
        @para blockID : the id of this machine. If None, then new unique ID is given.  
        @param nsl : next state logic function
        @param ol : output logic function
        @param startingState : the starting state of the moore machine
        @param risingEdge : boolean value if the block works on rising edge or falling edge
        @param clock : the clock object for this mealy machine
        @param nsl_delay : the delay in the next state logic
        @param ol_delay : the delay in the output logic
        @param register_delay : the delay in the register
        @return MealyMachine : the mealy machine instance. 
        """
        checkType([(plot, bool), (startingState, int), (risingEdge, bool), (nsl_delay, (int, float)), (ol_delay, (int, float))])

        self.__count += 1
        if (blockID == None):
            blockID = self.__makeUniqueID("Mealy")
        elif blockID in self.__uniqueIDlist:
            id = self.__makeUniqueID("Mealy")
            print(f"{blockID} is already used so changing to {id}")
            blockID = id

        self.__uniqueIDlist.append(blockID)
        temp = MealyMachine(env=self.__env, maxOutSize=maxOutSize, nsl=nsl, ol=ol, plot=plot, blockID=blockID, startingState=startingState, clk = clock, posEdge = risingEdge, nsl_delay = nsl_delay, ol_delay = ol_delay, register_delay = register_delay)
        self.__components.append(temp)
        return temp

    def clock(self, plot=False, blockID=None, timePeriod=1.2, onTime=0.6, initialValue=0):
        """
        Adds a clock to this class. 
        @param plot : boolean value whether to plot this clock or not
        @param blockID : the id of this clock. If None, then new unique ID is given.  
        @param timePeriod : the time period of this clock.
        @param onTime : the amount of time in each cycle that the clock shows high (1).
        @param initialValue : the initial value of the clock (default is 0)
        @return Clock : the clock instance
        """

        checkType([(plot, bool), (timePeriod, (int, float)), (onTime, (int, float))])

        self.__count += 1
        if (blockID == None):
            blockID = self.__makeUniqueID("Clock")
        elif blockID in self.__uniqueIDlist:
            id = self.__makeUniqueID("Clock")
            print(f"{blockID} is already used so changing to {id}")
            blockID = id

        self.__uniqueIDlist.append(blockID)
        temp = Clock(env=self.__env, maxOutSize=1, plot=plot, blockID=blockID, timePeriod=timePeriod, onTime=onTime, initialValue=initialValue)
        self.__components.append(temp)
        return temp

    def source(self, filePath: str, plot=False, blockID=None):
        """
        Adds an input block to this class.
        @param filePath : must be a valid filePath of type ".txt", ".csv", or ".xslx" to an input source.  
        @param plot : boolean value whether to plot this input source or not
        @param blockID : the id of this input block. If None, then new unique ID is given. 
        @return Input : the source instance.
        """

        inputList = InputGenerator(filePath).getInput()["Inputs"]
        self.__count += 1
        if (blockID == None):
            blockID = self.__makeUniqueID("Source")
        elif blockID in self.__uniqueIDlist:
            id = self.__makeUniqueID("Source")
            print(f"{blockID} is already used so changing to {id}")
            blockID = id

        self.__uniqueIDlist.append(blockID)
        temp = Input(inputList=inputList, env=self.__env, plot=plot, blockID=blockID)
        self.__components.append(temp)
        return temp

    def output(self, plot=True, blockID=None):
        """
        Adds an output block to this class.
        @param plot : boolean value whether to plot this output source or not
        @param blockID : the id of this input block. If None, then new unique ID is given.
        @return Output : the output object
        """
        self.__count += 1
        if (blockID == None):
            blockID = self.__makeUniqueID("Output")
        elif blockID in self.__uniqueIDlist:
            id = self.__makeUniqueID("Output")
            print(f"{blockID} is already used so changing to {id}")
            blockID = id

        self.__uniqueIDlist.append(blockID)
        temp = Output(env=self.__env, plot=plot, blockID=blockID)
        self.__components.append(temp)
        return temp

    def register(self, clock, delay, initalValue=0, plot=False, blockID=None):
        """
        @param clock : the clock object for this register
        @param delay : the delay in the register
        @param initialValue : the initial value of the register
        @param plot : boolean value whether to plot this register or not
        @param blockID : the id of this register. If None, then new unique ID is given.
        @return Register : the register object
        """
        self.__count += 1
        if (blockID == None):
            blockID = self.__makeUniqueID("Register")
        elif blockID in self.__uniqueIDlist:
            id = self.__makeUniqueID("Register")
            print(f"{blockID} is already used so changing to {id}")
            blockID = id
        
        self.__uniqueIDlist.append(blockID)
        return Register(env=self.__env, clock=clock, delay=delay, initialValue=initalValue, plot=plot, blockID=blockID)

    def run(self, until: int):
        """
        Runs each of the blocks that are added to this class for "until" time units. 
        If any block is not connected to an input source, then error is thrown.
        @param until : must be of type int and must specify the number of time units the block is supposed to run.
        @return : None
        """

        checkType([(until, int)])

        for i in self.__components:
            if (isinstance(i, HasOnlyOutputConnections) or i.isConnected()):
                i.run()
            else:
                printErrorAndExit(f"{i} is not connected.")

        self.__env.run(until=until)

        # plotting the plots
        for i in self.__components:
            i.plot()

        Block.plotter.show()

        # Generating csv file
        if self.__dump:
            self.__accumalateDump()
            dumpVars(Plotter.fillEmptyTimeSlots(self.__timeValues, self.__data), self.__name)

    def getEnv(self):
        """
        This method returns the environment of the current pydig object
        @return : simpy.Environment
        """
        return self.__env

    def generateCSV(self):
        """
        This method is used only when you want to dump all the variables in a (csv) file.
        @return : None
        """
        self.__dump = True

    def __accumalateDump(self):
        """
        This method accumalates the data from all blocks/components and creates a dump-able for them.
        @return : None
        """

        self.__data = {}
        self.__timeValues = set()

        for i in self.__components:
            vals = i.getScopeDump()
            self.__data.update(vals)

            discreteTimeValues = set(y[0] for x in vals for y in vals[x])
            self.__timeValues.update(discreteTimeValues)

        self.__timeValues.update([0, max(self.__timeValues) + 1])
        self.__timeValues = list(sorted(self.__timeValues))
