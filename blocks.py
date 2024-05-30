"""
This class is used for creating all the blocks.
It requires you to download simpy which can be done by

pip install simpy

@author Abhirath, Aryan, Gathik
@date 4/1/2023
@version 2.0
"""

from abc import ABC, abstractmethod
from utilities import checkType, printErrorAndExit
import simpy
import uuid
from pwlSource import InputGenerator
from scope import Plotter

class pydig: 
    """
    This class is used for adding your moore machines, input block, and output block.
    The manner in which the connections should occur is 
    Input Block --> Moore Machine 1 --> Moore Machine 2 --> .... --> Moore Machine n --> Output Block.
    The output of one moore machine can go to multiple moore machines.
    The moore machines and the output blocks can take multiple inputs. 

    This class does not perform the connections. See the classes Input, Machine, or Output for connecting purposes. 
    """

    def __init__(self, name="pydig"):
        """
        Creates a new simpy environment.
        @param name : the name of this object. 
        """

        self.__env = simpy.Environment()
        self.__components = []
        self.__name=name
        self.__dump = False

    def moore(self, maxOutSize, plot = False, blockID = "MooreMachine", nsl=None, ol=None, startingState = 0):
        """
        Adds a moore machine to this class. 
        @param maxOutSize : the maximum number of output wires
        @param plot : boolean value whether to plot this moore machine or not
        @para blockID : the id of this machine. If None, then new unique ID is given.  
        @param nsl : next state logic function
        @param ol : output logic function
        @param startingState : the starting state of the moore machine
        @return : the moore machine instance. 
        """

        checkType([(plot, bool), (startingState, int)])

        temp = Machine(self.__env, maxOutSize, nsl, ol, plot, blockID, startingState) 
        self.__components.append(temp)
        return temp

    def clock(self, plot=True, blockID=None, timePeriod=1.2, onTime = 0.6):
        """
        Adds a clock to this class. 
        @param plot : boolean value whether to plot this clock or not
        @param blockID : the id of this clock. If None, then new unique ID is given.  
        @param timePeriod : the time period of this clock.
        @param onTime : the amount of time in each cycle that the clock shows high (1).
        @return : the clock instance
        """

        checkType([(plot, bool), (timePeriod, (int, float)), (onTime, (int, float))])

        temp = Clock(self.__env, 1, plot, blockID, timePeriod, onTime) ########
        self.__components.append(temp)
        return temp
    
    def source(self, filePath:str, plot = True, blockID=None):
        """
        Adds an input block to this class.
        @param filePath : must be a valid filePath of type ".txt", ".csv", or ".xslx" to an input source.  
        @param plot : boolean value whether to plot this input source or not
        @param blockID : the id of this input block. If None, then new unique ID is given. 
        @return : the source instance.
        """
        
        inputList = InputGenerator(filePath).getInput()["Inputs"]

        temp = Input(inputList, self.__env, plot, blockID)
        self.__components.append(temp)
        return temp
    
    def output(self, plot = True, blockID=None):
        """
        Adds an output block to this class.
        @param plot : boolean value whether to plot this output source or not
        @param blockID : the id of this input block. If None, then new unique ID is given.
        @return : the output object
        """

        temp = Output(self.__env, plot, blockID)
        self.__components.append(temp)
        return temp
    
    def run(self, until:int):
        """
        Runs each of the blocks that are added to this class for "until" time units. 
        If any block is not connected to an input source, then error is thrown.
        @param until : must be of type int and must specify the number of time units the block is supposed to run.
        @return : None
        """

        checkType([(until, int)])

        for i in self.__components:
            if(isinstance(i, HasOnlyOutputConnections) or i.isConnected()):
                i.run()
            else:
                printErrorAndExit(f"{i} is not connected.")
        
        self.__env.run(until=until)

        # plotting the plots
        for i in self.__components:
            i.plot()
        
        Block.plotter.show()

        if self.__dump:
            self.accumalateDump()

            from utilities import dumpVars
            dumpVars(Plotter.fillEmptyTimeSlots(self.__timeValues, self.__data))
    
    def dumpVars(self):
        """
        This method is used only when you want to dump all the variables in a (csv) file.
        Currently there is no option and all the variables are dumped in a csv file located in the output folder
        which is created during runtime if not present.
        @return : None
        """
        self.__dump = True
    
    def accumalateDump(self):
        """
        This method accumalates the data from all blocks/components and creates a dump-able for them.

        this has no return value.
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

class ScopeDump():
    """
    This class is used for creating the scope. 
    All the different values that the user wants
    should be added to this class.
    """

    def __init__(self):
        """
        Creates a ScopeDumpy Object.
        """

        self.__values = {}

    def add(self, classification:str, time:float, value:int):
        """
        classification must be of type string and must specify
        what the value (time, value) represents. 
        time represents the time at which this value occured.
        value represents the value of the bus at this point.
        Adds (time, float) to classification.
        """
        
        checkType([(classification, str), (time, (float, int)), (value, int)])

        if(classification in self.__values):
            self.__values[classification].append((time, value))
        else:
            self.__values[classification] = [(time, value)]
    
    def getValues(self):
        """
        Returns all the values added to this class.
        """

        return dict(self.__values)

class Block(ABC):
    """
    This class specifies the methods and variables that are common to each block.
    It includes some abstract methods that should be implemented by its subclasses.
    """

    __uniqueIDlist = []
    plotter = Plotter()

    def __init__(self, env:simpy.Environment, plot:bool, blockID:str):
        """
        env is the simpy environment.
        blockID is the id of this input block, It serves as a name for this block.
        """
        
        self._env = env
        self._scopeDump = ScopeDump()
        self.__plot = plot
        self._blockID = blockID
    
    def getBlockID(self):
        """
        Returns the block ID of the current block.
        """
        
        return self._blockID
    
    def getScopeDump(self):
        """
        Returns the scope dump values for this block.
        """

        return self._scopeDump.getValues()

    @staticmethod
    def __uniqueID(blockID):
        """
        Creates a unique ID for each block
        """

        if(blockID != None and blockID in Block.__uniqueIDlist):
            printErrorAndExit(f"{blockID} has already been used as an ID for another block.")
        elif(blockID == None):
            blockID = uuid.uuid4()
        
        Block.__uniqueIDlist.append(blockID)

        return blockID

    def plot(self):
        """
        plots the values that are associated to the block that has
        called this method.
        """

        if self.__plot:
            Block.plotter.plot(self.getScopeDump(), f"Plot of {self._blockID}")
    
    @abstractmethod
    def __str__(self):
        """
        Should return a string representation of the block.
        """
        
        pass
    
    @abstractmethod
    def __le__(self, other):
        """
        Should allow for connections between blocks.
        """
        
        pass

    @abstractmethod
    def run(self):
        """
        Should specify how to run this block.
        """
        
        pass

class HasInputConnections(Block):
    """
    A HasInputConnections block is a block that has input connection wires. 
    Thus only Machine and Output are functional blocks because they
    are the only ones that take an input connection wire. 
    To connect a block b1 to HasInputConnections b2 such that the
    output of b1 goes to the input of b2, write: "b2 <= b1".
    Block b1 must be of type HasOutputConnections. 
    """
    
    def __init__(self, env, plot, blockID):
        """
        env is the simpy environment.  
        plot is a boolean value whether to plot this block or not. 
        blockID is the id of this input block. If None, 
        then new unique ID is given.
        """
        
        super().__init__(env, plot, blockID)

        self._trigger = simpy.Store(self._env)
        self._input = []
        self._inputSizes = []
        self._inputCount = 0
        self._isConnected = False
        self._connectedID = []
        self._clockID = None
        
    def __le__(self, other):
        """
        other must be of type HasOutputConnections. 
        The output of other goes into the input of self.
        If the inputs of self are already connected, then error is generated.
        """
        if(isinstance(self, Machine) and isinstance(other, Clock)):
            self.clk = other._output
            self._clockID = other.addFanout()
            return True

        checkType([(other, (HasOutputConnections))])
        self._input.append(other._output)
        self._inputSizes.append((other.getLeft(), other.getRight(), other.getWidth()))
        self._inputCount += 1
        self._connectedID.append(other.addFanout())
        self._isConnected = True
        other.resetState()
        return True

    def getInputCount(self):
        return self._inputCount

    def _strip(self, val, left, right):
        temp = (val >> right) << right
        val -= temp
        val = val >> left
        return val
    
    def getInputVal(self):
        ans = 0
        factor = 1
        for i in range(self._inputCount):
            ans += self._strip(self._input[i][0], self._inputSizes[i][0], self._inputSizes[i][1]) * factor
            factor = factor * (2 ** self._inputSizes[i][2])
        return ans
    
    def isConnectedToInput(self):
        """
        Returns true if this block is connected to input.
        False otherwise.
        """
        return self._isConnected
    
    @abstractmethod
    def isConnected(self):
        """
        Returns true if this block is connected to everything.
        False otherwise.
        """
        pass

    def runTriggers(self):
        """
        Readys all the triggering processes
        """
        for i in range(self.getInputCount()):
            self._env.process(self.__runTriggers(self._trigger, self._input[i][self._connectedID[i]]))

    def __runTriggers(self,triggerObj,checkObj):
        while True:
            yield checkObj.get()
            if (len(triggerObj.items)<1):
                triggerObj.put(True)            
    
    def input(self, left=None, right=None):
        """
        Returns the instance of this class for connection purposes.
        """
        return self

class HasOutputConnections(Block):
    """
    A HasOutputConnections block is a block that has output connection wires. 
    Thus only Machine and Input are functional blocks because they
    are the only ones that have an output connection wire. 
    """
    
    def __init__(self, env, maxOutSize, plot, blockID):
        """
        env is the simpy environment.  
        blockID is the id of this input block. If None, 
        then new unique ID is given.
        """

        super().__init__(env, plot, blockID)

        self._maxOutSize = maxOutSize
        self._state = (0, maxOutSize, maxOutSize)
        self.defineFanOut()

    def resetState(self):
        self._state = (0, self._maxOutSize, self._maxOutSize)

    def getLeft(self):
        return self._state[0]
        
    def getRight(self):
        return self._state[1]
        
    def getWidth(self):
        return self._state[2]
    
    def defineFanOut(self):
        """
        Defines the fan out variables.
        Fan out represents the blocks which
        are connected to this block.
        """
        
        self._fanOutCount = 0
        self._output = [0] # here the first element is the value itself, and the rest of the elements will be the simpy.Store() objects for the other machines connected to it

    def addFanout(self):
        """
        Adds an output wire to this block. 
        """
        self._fanOutCount += 1
        self._output.append(simpy.Store(self._env))
        self._output[-1].put(True)
        return self._fanOutCount

    def __gt__(self, other):
        """
        Makes it possible to do the following connection:
        
        object1.output > object2.input
        """
        
        return other <= self

    def output(self, left = 0, right = None):
        """
        Returns the instance of this class for connection purposes.
        """
        if (right == None):
            right = self._maxOutSize

        self._state = (left, right, right - left)
        return self

class HasOnlyOutputConnections(HasOutputConnections):
    """
    Class used by only those classes that only have output connections.
    These classes don't take any input.
    """
    
    def __init__(self, env, maxOutSize, plot, blockID):
        """
        env is the simpy environment.
        plot is a boolean variable which represents whether or not we should plot this class.
        blockID is the id of this input block. If None, 
        then new unique ID is given.
        """
        super().__init__(env, maxOutSize, plot, blockID)
    
    def __le__(self, other):
        """
        We are not allowed to connect anything that goes into the input block.
        """

        printErrorAndExit(f"Cannot connect {self} to {other}.")
    
    @abstractmethod
    def _go(self):
        """
        This method generates the next output based on certain conditions.
        """

        pass

    def run(self):
        """
        Runs this block.
        """
        
        self._env.process(self._go())
    

class Machine(HasInputConnections, HasOutputConnections):
    """
    A machine is both a HasInputConnections block and a HasOutputConnections block.
    This represents the Moore Machine.
    """
    
    def __init__(self, env, maxOutSize, nsl, ol, plot, blockID, startingState = 0):
        """
        env must be a simpy environment.
        clock must be of type Clock.
        nsl must be a valid function specifying next state logic.
        ol must be a valid function specifying output logic.
        blockID is the id of this input block. If None, 
        then new unique ID is given.
        """
        
        HasInputConnections.__init__(self, env, plot, blockID)
        HasOutputConnections.__init__(self, env, maxOutSize, plot, blockID)
        self.resetState()
        self.nsl = nsl
        self.ol = ol
        self.presentState = startingState
        self.nextState = startingState
        self._Pchange = simpy.Store(self._env)
        self._Pchange.put(False)

    def __str__(self):
        """
        Returns a string representation of this machine.
        """
        
        return f"Machine ID {self._blockID}"
    
    def __runNSL(self):
        """
        Runs the next state logic if the input to this machine changed.
        """
        
        while True:
            yield self._trigger.get()
            
            # adding the inputs to scopedump
            self._scopeDump.add(f"Input to {self.getBlockID()}", self._env.now, self.getInputVal())

            # running the NSL
            tempout = self.nsl(self.presentState, self.getInputVal())
            yield self._env.timeout(0.1)
            
            # updating the next State
            self.nextState = tempout
            self._scopeDump.add(f"NS of {self.getBlockID()}", self._env.now, self.nextState)
    
    # not in use as of now
    def __runNSLp(self):
        """
        Runs the next state logic if the present state changed. 
        """
        
        while True:
            yield self._Pchange.get()
            
            # running the NSL
            tempout = self.nsl(self.presentState, self.getInputVal())
            yield self._env.timeout(0.1)
            
            # updating the output
            self.nextState = tempout
            self._scopeDump.add(f"NS of {self.getBlockID()}", self._env.now, self.nextState)

    def __runReg(self):
        """
        Registers run based on clock.
        TODO: Make it run based on clock.
        """
        while True:
            yield self.clk[self._clockID].get()
            if self.presentState == self.nextState:
                continue
            yield self._env.timeout(0.1)
            self.presentState = self.nextState
            self._scopeDump.add(f"PS of {self.getBlockID()}", self._env.now, self.presentState)
            self._Pchange.put(True)
            self._env.process(self.__runOL())

    def __runOL(self):
        """
        Output logic runs when the output value is changed.
        TODO: Make it run based on output logic. 
        """
        temp = self.ol(self.presentState)
        yield self._env.timeout(0.1) 
        self._output[0] = temp
        self._scopeDump.add(f"output of {self.getBlockID()}", self._env.now, self._output[0])
        # triggering events for the connected machines
        for i in range(1, self._fanOutCount + 1):
            self._output[i].put(True)

    
    def run(self):
        """
        Runs this block.
        """
        
        self._env.process(self.__runNSL())
        self._env.process(self.__runReg())
        self._env.process(self.__runNSLp())
        self.runTriggers()
    
    def isConnected(self):

        return self.clk != None and self.nsl != None and self.ol != None and self.isConnectedToInput()

    def clock(self):
        return self
    
class Input(HasOnlyOutputConnections):
    """
    An input is a HasOutputConnections block.
    This represents the Input Block.
    """
    
    def __init__(self, inputList:list, env, plot, blockID):
        """
        inputList must be a list that contains the input changes at the time intervals.
        env is the simpy environment.
        blockID is the id of this input block. If None, 
        then new unique ID is given.
        """
        maxOutSize = 2
        for i in inputList:
            if (len(bin(i[1])) > maxOutSize):
                maxOutSize = len(bin(i[1]))
        maxOutSize-=2
        super().__init__(env, maxOutSize, plot, blockID)
        self._input = inputList
    
    def __str__(self):
        """
        Returns the string representation of this input block.
        """
        
        return f"Input ID {self._blockID}"
    
    def _go(self):
        """
        Runs the input at every change in input value specified by inputList.
        """
        
        for i in self._input:

            yield self._env.timeout(i[0]-self._env.now)
            
            self._output[0]=i[1]
            
            for i in range(1,self._fanOutCount+1):
                self._output[i].put(True)

            self._scopeDump.add(f"Input to {self.getBlockID()}", self._env.now, self._output[0])

class Clock(HasOnlyOutputConnections):
    """
    TODO: Create a clock.
    """

    def __init__(self, env, maxOutSize, plot, blockID, timePeriod = 1.2, onTime = 0.6):
        super().__init__(env, maxOutSize, plot, blockID)

        checkType([(timePeriod,(int, float)), (onTime, (int, float))])

        if(timePeriod < onTime):
            printErrorAndExit(f"Clock {self} cannot have timePeriod = {timePeriod} less than onTime = {onTime}.")

        self.__timePeriod = timePeriod
        self.__onTime = onTime
        self._output[0]=0

    def output(self, left = None, right = None):
        """
        Returns this object for connection purposes.
        """
        return self

    def __str__(self):
        return f"Clock ID {self._blockID}"

    def _go(self):
        while True:
            yield self._env.timeout((1-self._output[0])*(self.__timePeriod - self.__onTime)+self._output[0]*(self.__onTime))

            self._output[0] = 1 - self._output[0]

            if(self._output[0]):
                for i in range(1,self._fanOutCount+1):
                    self._output[i].put(True)

            self._scopeDump.add(f"Clock {self.getBlockID()}", self._env.now, self._output[0])

    def addFanout(self):
        """
        Adds an output wire to this block. 
        """
        self._fanOutCount += 1
        self._output.append(simpy.Store(self._env))
        self._output[-1].put(True)
        return self._fanOutCount

class Output(HasInputConnections):
    """
    An Output is a HasInputConnections block.
    This represents the Output Block.
    blockID is the id of this input block. If None, 
    then new unique ID is given.
    """

    def __init__(self, env, plot, blockID):
        """
        env is a simpy environment.
        """
        
        super().__init__(env, plot, blockID)
    
    def __str__(self):
        """
        Returns a string representation of the output block.
        """
        
        return f"Output ID {self._blockID}"
        
    def __give(self):
        """
        Adds the output value to this class every time there is a change in it.
        """
        
        while True:
            yield self._trigger.get()
            self._scopeDump.add(f"Final Output from {self.getBlockID()}", self._env.now, self.getInputVal())
    
    def run(self):
        """
        Runs the output block
        """
        
        self._env.process(self.__give())
        self.runTriggers()
    
    def isConnected(self):
        return self.isConnectedToInput() 

if __name__ == "__main__":
    def NSL1(i, ps):
        return 0

    def NSL2(i, ps):
        return 0

    def OL1(ps):
        return 0

    def OL2(ps):
        return 0

    # Creating a pydig class and adding all the blocks to it.
    pydig = pydig()
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
    pydig.run(until = 21)
