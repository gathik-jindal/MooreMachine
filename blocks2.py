"""
This class is used for creating all the blocks.
It requires you to download simpy which can be done by

pip install simpy

@author: Abhirath, Aryan, Gathik
@date: 27/12/2023
@version: 1.0
"""

from abc import ABC, abstractmethod
from utilities import checkType, printErrorAndExit
from pwlSource import InputGenerator
import simpy
import uuid

class Manager: 
    """
    This class is used for adding your moore machines, input block, and output block.
    The manner in which the connections should occur is 
    Input Block --> Moore Machine 1 --> Moore Machine 2 --> .... --> Moore Machine n --> Output Block.
    The output of one moore machine can go to multiple moore machines. 
    In version 1.0, however, one moore machine can only take input from only one machine. 
    Thus, in each block, there can only be one input wires, but there can be multiple output wires.

    TODO : Make version 2 that uses Bus to combine different inputs after everything else is complete.

    This class does not perform the connections. See the classes Input, Machine, or Output for connecting purposes. 
    """

    def __init__(self):
        """
        Creates a new simpy environment.
        """

        self.__env = simpy.Environment()
        self.__components = []

    def addMachine(self, clock, nsl, ol, blockID=None):
        """
        Adds a moore machine to this class. 
        clock must be of type Clock.
        nsl must be of type NSL.
        ol must be of type OL.
        blockID is the id of this machine. If None, 
        then new unique ID is given.  
        """

        checkType([(clock, Clock)])

        temp = Machine(self.__env, clock, nsl, ol, blockID)
        self.__components.append(temp)
        return temp

    def addInput(self, filePath:str, blockID=None):
        """
        Adds an input block to this class.
        filePath must be a valid filePath of type
        ".txt", ".csv", or ".xslx" to an input source.  
        blockID is the id of this input block. If None, 
        then new unique ID is given. 
        """
        
        inputList = InputGenerator(filePath).getInput()["Inputs"]

        temp = Input(inputList, self.__env, blockID)
        self.__components.append(temp)
        return temp
    
    def addOutput(self, blockID=None):
        """
        Adds an output block to this class.
        blockID is the id of this input block. If None, 
        then new unique ID is given. 
        """

        temp = Output(self.__env, blockID)
        self.__components.append(temp)
        return temp
    
    def run(self, until:int):
        """
        Runs each of the blocks that are added to this class.
        until must be of type int and must specify the number
        of time units the block is supposed to run.
        If any block is not connected to an input source, then error
        is thrown.
        """

        checkType([(until, int)])

        for i in self.__components:
            if(isinstance(i, Input) or i.isConnected()):
                i.run()
            else:
                printErrorAndExit(f"{i} is not connected.")
        
        self.__env.run(until=until)

class ScopeDump:
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

    def __init__(self, env, blockID = None):
        """
        env is the simpy environment.  
        blockID is the id of this input block. If None, 
        then new unique ID is given.
        """
        
        self._env = env
        self._scopeDump = ScopeDump()
        
        self._blockID = Block.__uniqueID(blockID)


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
        
        
    def getBlockID(self):
        """
        Returns the block ID of the current block.
        """
        
        return self._blockID
    
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
    
    def getScopeDump(self):
        """
        Returns the scope dump values for this block.
        """

        return self._scopeDump.getValues()

class HasInputConnections(Block):
    """
    A HasInputConnections block is a block that has input connection wires. 
    Thus only Machine and Output are functional blocks because they
    are the only ones that take an input connection wire. 
    To connect a block b1 to HasInputConnections b2 such that the
    output of b1 goes to the input of b2, write: "b2 <= b1".
    Block b1 must be of type HasOutputConnections. 
    """
    
    def __init__(self, env, blockID=None):
        """
        env is the simpy environment.  
        blockID is the id of this input block. If None, 
        then new unique ID is given.
        """
        
        super().__init__(env, blockID)
    
        self._isConnected = False
        self._connectedID = None
        self._input = None
    
    def __le__(self, other):
        """
        other must be of type HasOutputConnections. 
        The output of other goes into the input of self.
        If the inputs of self are already connected, then error is generated.
        """
        
        if(self._isConnected):
            printErrorAndExit(self, " is already connected.")

        checkType([(other, (HasOutputConnections))])

        self._input = other._output
        self._connectedID = other.addFanout()
        self._isConnected = True
        
        return True

    def isConnected(self):
        """
        Returns true if this block is connected.
        False otherwise.
        """
        
        return self._isConnected

class HasOutputConnections(Block):
    """
    A HasOutputConnections block is a block that has output connection wires. 
    Thus only Machine and Input are functional blocks because they
    are the only ones that have an output connection wire. 
    """
    
    def __init__(self, env, blockID=None):
        """
        env is the simpy environment.  
        blockID is the id of this input block. If None, 
        then new unique ID is given.
        """

        super().__init__(env, blockID)

        self.defineFanOut()
    
    def defineFanOut(self):
        """
        Defines the fan out variables.
        Fan out represents the blocks which
        are connected to this block.
        """
        
        self._fanOutCount = 0
        self._output = [0]
    
    def addFanout(self):
        """
        Adds an output wire to this block. 
        """
        
        self._fanOutCount += 1
        self._output.append(simpy.Store(self._env))
        self._output[-1].put(True)
        return self._fanOutCount

class Machine(HasInputConnections, HasOutputConnections):
    """
    A machine is both a HasInputConnections block and a HasOutputConnections block.
    This represents the Moore Machine.
    """
    
    def __init__(self, env, clock, nsl, ol, blockID=None):
        """
        env must be a simpy environment.
        clock must be of type Clock.
        nsl must be a valid function specifying next state logic.
        ol must be a valid function specifying output logic.
        blockID is the id of this input block. If None, 
        then new unique ID is given.
        """
        
        super().__init__(env, blockID)
        self.defineFanOut()

        self._clock = clock
        self._NSL = nsl
        self._OL = ol
        self._Pchange = simpy.Store(self._env)
    
    def __str__(self):
        """
        Returns a string representation of this machine.
        """
        
        return f"Machine ID {self._blockID}"
    
    def __runNSLi(self):
        """
        Runs the next state logic if the input to this machine changed.
        """
        
        while True:
            yield self._input[self._connectedID].get()
            
            self._scopeDump.add("Input", self._env.now, self._input[0])

            tempout = self._input[0] + 1
            yield self._env.timeout(0.6)
            
            self._output[0] = tempout

            for i in range(1, self._fanOutCount + 1):
                self._output[i].put(True)
            
            self._scopeDump.add("NS", self._env.now, self._output[0])
    
    def __runNSLp(self):
        """
        Runs the next state logic if the present state changed. 
        """
        
        while True:
            yield self._Pchange.get()
            
            print("recalculate at ", self._env.now, "using", self._input[1])
            
            yield self._env.timeout(0.5)
            
            self._output[1] = self._input[1] + 1
            self._output[0].put(True)
    
    def __runReg(self):
        """
        Registers run based on clock.
        TODO: Make it run based on clock.
        """
        
        pass

    def __runOL(self):
        """
        Output logic runs when the output value is changed.
        TODO: Make it run based on output logic. 
        """
        
        pass
    
    def run(self):
        """
        Runs this block.
        """
        
        self._env.process(self.__runNSLi())

class Input(HasOutputConnections):
    """
    An input is a HasOutputConnections block.
    This represents the Input Block.
    """
    
    def __init__(self, inputList:list, env, blockID=None):
        """
        inputList must be a list that contains the input changes at the time intervals.
        env is the simpy environment.
        blockID is the id of this input block. If None, 
        then new unique ID is given.
        """
        
        super().__init__(env, blockID)
        self._input = inputList
    
    def __str__(self):
        """
        Returns the string representation of this input block.
        """
        
        return f"Input ID {self._blockID}"

    def __le__(self, other):
        """
        We are not allowed to connect anything that goes into the input block.
        """

        printErrorAndExit(f"Cannot connect {self} to {other}.")
    
    def __go(self):
        """
        Runs the input at every change in input value specified by inputList.
        """
        
        for i in self._input:

            yield self._env.timeout(i[0]-self._env.now)
            
            self._output[0]=i[1]
            
            for i in range(1,self._fanOutCount+1):
                self._output[i].put(True)

            self._scopeDump.add("Input", self._env.now, self._output[0])

    def run(self):
        """
        Runs this block.
        """
        
        self._env.process(self.__go())

class Output(HasInputConnections):
    """
    An Output is a HasInputConnections block.
    This represents the Output Block.
    blockID is the id of this input block. If None, 
    then new unique ID is given.
    """

    def __init__(self, env, blockID=None):
        """
        env is a simpy environment.
        """
        
        super().__init__(env, blockID)
    
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
            yield self._input[self._connectedID].get()
            self._scopeDump.add("Output", self._env.now, self._input[0])
    
    def run(self):
        """
        Runs the output block
        """
        
        self._env.process(self.__give()) 

class Clock:
    """
    TODO: Create a clock.
    """
    pass

if __name__ == "__main__":

    #Creating a manager class and adding all the blocks to it.
    manager = Manager()
    i = manager.addInput("Tests\\Test.txt", "input 1")
    m1 = manager.addMachine(Clock(), 1, 1, "m1")
    m2 = manager.addMachine(Clock(), 1, 1, "m2")
    o = manager.addOutput("output")

    #Making all the connections
    m1 <= i
    m2 <= m1
    o <= m2

    #Running all the blocks.
    manager.run(until = 40)
    print("InputBlock:", i.getScopeDump())
    print("Machine M1:", m1.getScopeDump())
    print("Machine M2:", m2.getScopeDump())
    print("OutputBlock:", o.getScopeDump())
