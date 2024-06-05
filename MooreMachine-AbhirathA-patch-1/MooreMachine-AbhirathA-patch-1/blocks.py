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
from utilities import fillEmptyTimeSlots, dumpVars
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
    In version 1.0, however, one moore machine can only take input from only one machine. 
    Thus, in each block, there can only be one input wires, but there can be multiple output wires.

    This class does not perform the connections. See the classes Input, Machine, or Output for connecting purposes. 
    """

    def __init__(self, name="pydig"):
        """
        Creates a new simpy environment.
        @param name : the name of this object. 
        """

        self.__env = simpy.Environment()
        self.__components = []
        self.__name = name
        self.__dump = False

    def moore(self, plot=False, blockID=None, nsl=None, ol=None):
        """
        Adds a moore machine to this class. 
        @param plot : boolean value whether to plot this moore machine or not
        @para blockID : the id of this machine. If None, then new unique ID is given.  
        @param nsl : next state logic function
        @param ol : output logic function
        @return : the moore machine instance. 
        """

        checkType([(plot, bool)])

        temp = Machine(self.__env, nsl, ol, plot, blockID)
        self.__components.append(temp)
        return temp

    def clock(self, plot=True, blockID=None, timePeriod=1.2, onTime=0.6):
        """
        Adds a clock to this class. 
        @param blockID : the id of this machine. If None, then new unique ID is given.  
        @param timePeriod : the time period of this clock.
        @param onTime : the amount of time in each cycle that the clock shows high (1).
        @return : the clock instance
        """

        checkType([(plot, bool), (timePeriod, (int, float)),
                  (onTime, (int, float))])

        temp = Clock(self.__env, plot, blockID, timePeriod, onTime)
        self.__components.append(temp)
        return temp

    def source(self, filePath: str, blockID=None):
        """
        Adds an input block to this class.
        @param filePath : must be a valid filePath of type ".txt", ".csv", or ".xslx" to an input source.  
        @param blockID : the id of this input block. If None, then new unique ID is given. 
        @return : the source instance.
        """

        inputList = InputGenerator(filePath).getInput()["Inputs"]

        temp = Input(inputList, self.__env, False, blockID)
        self.__components.append(temp)
        return temp

    def output(self, blockID=None):
        """
        Adds an output block to this class.
        @param blockID : the id of this input block. If None, then new unique ID is given.
        @return : the output object
        """

        temp = Output(self.__env, True, blockID)
        self.__components.append(temp)
        return temp

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
        dump = Block.dumpAll()

        dump = fillEmptyTimeSlots(dump)

        if self.__dump:
            dumpVars(dump)

        plot = Plotter()

        plot.plot(dump, f"Plot of {self.__name}")
        plot.show()

    def dumpVars(self):
        """
        This method is used only when you want to dump all the variables in a (csv) file.
        Currently there is no option and all the variables are dumped in a csv file located in the output folder
        which is created during runtime if not present.
        @return : None
        """
        self.__dump = True


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

    def add(self, classification: str, time: float, value: int):
        """
        classification must be of type string and must specify
        what the value (time, value) represents. 
        time represents the time at which this value occured.
        value represents the value of the bus at this point.
        Adds (time, float) to classification.
        """

        checkType([(classification, str), (time, (float, int)), (value, int)])

        if (classification in self.__values):
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
    __dumpList = []
    __dump = {}

    def __init__(self, env, plot, blockID=None):
        """
        env is the simpy environment.
        blockID is the id of this input block. If None, 
        then new unique ID is given.
        """

        self._env = env
        self._scopeDump = ScopeDump()

        if plot == True:
            Block.__dumpList.append(self)

        self._blockID = Block.__uniqueID(blockID)

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

        if (blockID != None and blockID in Block.__uniqueIDlist):
            printErrorAndExit(
                f"{blockID} has already been used as an ID for another block.")
        elif (blockID == None):
            blockID = uuid.uuid4()

        Block.__uniqueIDlist.append(blockID)

        return blockID

    @staticmethod
    def dumpAll():
        """
        Returns all the values to be plotted
        """

        for i in Block.__dumpList:
            Block.__dump.update(i.getScopeDump())
        return Block.__dump

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

    def __init__(self, env, plot, blockID=None):
        """
        env is the simpy environment.  
        blockID is the id of this input block. If None, 
        then new unique ID is given.
        """

        super().__init__(env, plot, blockID)

        self._input = []
        self._inputSizes = []
        self._inputCount = 0
        self._isConnected = False
        self._connectedID = None
        self._clockID = None

    def __le__(self, other):
        """
        other must be of type HasOutputConnections. 
        The output of other goes into the input of self.
        If the inputs of self are already connected, then error is generated.
        """
        if (isinstance(self, Machine) and isinstance(other, Clock)):
            self.clk = other._output
            self._clockID = other.addFanout()
            return True

        if (self.isConnectedToInput()):
            printErrorAndExit(self, " is already connected.")

        checkType([(other, (HasOutputConnections))])

        self._input.append(other._output)
        self._inputSizes.append(
            (other.getLeft(), other.getRight(), other.getWidth()))
        self._inputCount += 1
        self._connectedID = other.addFanout()
        self._isConnected = True

        return True

    def getInputCount(self):
        return self._inputCount

    def getInputVal(self):
        ans = 0
        factor = 1
        for i in range(self._inputCount):
            ans += self._input[i][0] * factor
            factor = factor * (10 ** self._inputSize[i][2])
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

    def __init__(self, env, plot, blockID=None):
        """
        env is the simpy environment.  
        blockID is the id of this input block. If None, 
        then new unique ID is given.
        """

        super().__init__(env, plot, blockID)

        self.defineFanOut()

    def defineFanOut(self):
        """
        Defines the fan out variables.
        Fan out represents the blocks which
        are connected to this block.
        """

        self._fanOutCount = 0
        # here the first element is the value itself, and the rest of the elements will be the simpy.Store() objects for the other machines connected to it
        self._output = [0]

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

    def output(self, left=None, right=None):
        """
        Returns the instance of this class for connection purposes.
        """
        return self


class HasOnlyOutputConnections(HasOutputConnections):
    """
    Class used by only those classes that only have output connections.
    These classes don't take any input.
    """

    def __init__(self, env, plot, blockID):
        """
        env is the simpy environment.
        plot is a boolean variable which represents whether or not we should plot this class.
        blockID is the id of this input block. If None, 
        then new unique ID is given.
        """
        super().__init__(env, plot, blockID)

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

    def __init__(self, env, nsl, ol, plot=False, blockID=None):
        """
        env must be a simpy environment.
        clock must be of type Clock.
        nsl must be a valid function specifying next state logic.
        ol must be a valid function specifying output logic.
        blockID is the id of this input block. If None, 
        then new unique ID is given.
        """

        super().__init__(env, plot, blockID)

        self.nsl = nsl
        self.ol = ol
        self.presentState = 0
        self.nextState = 0
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
            yield self._input[self._connectedID].get()

            # adding the inputs to scopedump
            self._scopeDump.add(
                f"Input to {self.getBlockID()}", self._env.now, self._input[0])

            # running the NSL
            tempout = self.nsl(self.presentState, self._input[0])
            yield self._env.timeout(0.1)

            # updating the next State
            self.nextState = tempout
            self._scopeDump.add(
                f"NS of {self.getBlockID()}", self._env.now, self.nextState)

    # not in use as of now
    def __runNSLp(self):
        """
        Runs the next state logic if the present state changed. 
        """

        while True:
            yield self._Pchange.get()

            # running the NSL
            tempout = self.nsl(self.presentState, self._input[0])
            yield self._env.timeout(0.1)

            # updating the output
            self.nextState = tempout
            self._scopeDump.add(
                f"NS of {self.getBlockID()}", self._env.now, self.nextState)

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

            self._scopeDump.add(
                f"PS of {self.getBlockID()}", self._env.now, self.presentState)
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
        self._scopeDump.add(
            f"output of {self.getBlockID()}", self._env.now, self._output[0])
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
        self._env.process(self.__runOL())

    def isConnected(self):

        return self.clk != None and self.nsl != None and self.ol != None and self.isConnectedToInput()

    def clock(self):
        return self


class Input(HasOnlyOutputConnections):
    """
    An input is a HasOutputConnections block.
    This represents the Input Block.
    """

    def __init__(self, inputList: list, env, plot=False, blockID=None):
        """
        inputList must be a list that contains the input changes at the time intervals.
        env is the simpy environment.
        blockID is the id of this input block. If None, 
        then new unique ID is given.
        """

        super().__init__(env, plot, blockID)
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

            self._output[0] = i[1]

            for i in range(1, self._fanOutCount+1):
                self._output[i].put(True)

            self._scopeDump.add(
                f"Input to {self.getBlockID()}", self._env.now, self._output[0])


class Clock(HasOnlyOutputConnections):
    """
    TODO: Create a clock.
    """

    def __init__(self, env, plot=True, blockID=None, timePeriod=1.2, onTime=0.6):
        super().__init__(env, plot, blockID)

        checkType([(timePeriod, (int, float)), (onTime, (int, float))])

        if (timePeriod < onTime):
            printErrorAndExit(f"Clock {self} cannot have timePeriod = {
                              timePeriod} less than onTime = {onTime}.")

        self.__timePeriod = timePeriod
        self.__onTime = onTime
        self._output[0] = 0

    def output(self):
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

            if (self._output[0]):
                for i in range(1, self._fanOutCount+1):
                    self._output[i].put(True)

            self._scopeDump.add(
                f"Clock {self.getBlockID()}", self._env.now, self._output[0])

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

    def __init__(self, env, plot=True, blockID=None):
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
            yield self._input[self._connectedID].get()
            self._scopeDump.add(f"Final Output from {
                                self.getBlockID()}", self._env.now, self._input[0])

    def run(self):
        """
        Runs the output block
        """

        self._env.process(self.__give())

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
    m1 = pydig.moore(plot=True, blockID="m1")
    m2 = pydig.moore(plot=True, blockID="m2")
    o = pydig.output(blockID="out")

    print(i, m1, m2, o, sep="\n")

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
    pydig.run(until=21)
