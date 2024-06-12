#### Everything is a clock

"""
This file contains the classes that are used to create the blocks.
It requires you to download simpy.

The objects that it defines are:

    Block: This class specifies the methods and variables that are common to each block.
    HasInputConnections: A HasInputConnections block is a block that has input connection wires.
    HasOutputConnections: A HasOutputConnections block is a block that has output connection wires.
    HasOnlyOutputConnections: Class used by only those classes that only have output connections.
    Machine: The Moore Machine object.
    Input: A block that generates an input signal.
    Clock: A block that generates a clock signal.
    Output: An output block that generates an output signal.
    Combinational: This block is used to create a logic block.

@author Abhirath, Aryan, Gathik
@date 4/12/2023
@version 1.6
"""

from abc import ABC, abstractmethod
from utilities import checkType, printErrorAndExit
import simpy
from scope import Plotter, ScopeDump

timeout = 0.1


class Block(ABC):
    """
    This class specifies the methods and variables that are common to each block.
    It includes some abstract methods that should be implemented by its subclasses.
    """
    plotter = Plotter()

    def __init__(self, **kwargs):
        """
        Use keyword arguments to pass the following parameters:
        @param env : is the simpy environment.
        @param blockID : is the id of this input block, It serves as a name for this block.
        @param plot : is a boolean variable which represents whether or not we should plot this class.
        """

        self._env = kwargs.get("env", None)
        self._scopeDump = ScopeDump()
        self.__plot = kwargs.get("plot", False)
        self.__blockID = kwargs.get("blockID", 0)

    def getBlockID(self):
        """
        Returns the block ID of the current block.
        @return str : blockID
        """
        return self.__blockID

    def setBlockID(self, i):
        """
        Changes the block ID of the current block.
        @return str : blockID
        """
        self.__blockID = i
        return self.__blockID


    def getScopeDump(self):
        """
        Returns the scope dump values for this block.
        @return dict : of all the values that it has stored.
        """
        return self._scopeDump.getValues()

    def plot(self):
        """
        plots the values if plot=True was passed inthat are
        associated to the block that has called this method.
        @return : None
        """
        if self.__plot:
            Block.plotter.plot(self.getScopeDump(), f"Plot of {self.getBlockID()}")

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
    To connect a block b1 to HasInputConnections b2 such that the
    output of b1 goes to the input of b2, write: "b2 <= b1".
    Block b1 must be of type HasOutputConnections. 
    """

    def __init__(self, **kwargs):
        """
        Use keyword arguments to pass the following parameters:
        @param env : is the simpy environment.
        @param plot : is a boolean value whether to plot this block or not.
        @param blockID : is the id of this input block. If blockID is a duplicate
                         or is not given, then new unique ID is given.
        """
        self.__input = []
        self.__inputSizes = []
        self.__inputCount = 0
        self.__isConnected = False
        super().__init__(**kwargs)

    def __le__(self, other):
        """
        The output of other goes into the input of self.
        If the inputs of self are already connected, then error is generated.

        @param other : must be of type HasOutputConnections.
        @return bool : True
        """

        checkType([(other, (HasOutputConnections))])
        self.__input.append(other._output)
        self.__inputSizes.append((other.getLeft(), other.getRight(), other.getWidth()))
        self.__inputCount += 1
        self.__isConnected = True
        other.addFanOut(self)
        other.resetState()
        return True

    def getInputCount(self):
        """
        @return int: the number of inputs connected to this block.
        """
        return self.__inputCount

    def __strip(self, val, left, right):
        """
        Strips the value to get the required bits.
        @param val : the value to be stripped.
        @param left : the LSB required (inclusive).
        @param right : the MSB not required (exclusive).
        @return int : The final value only with the required bits
        """

        temp = (val >> right) << right
        val -= temp
        val = val >> left
        return val

    def getInputVal(self):
        """
        @return int : the final value of the input connected to this block.
        """
        ans = 0
        factor = 1
        for i in range(self.__inputCount):
            ans += self.__strip(self.__input[i][0], self.__inputSizes[i][0], self.__inputSizes[i][1]) * factor
            factor = factor * (2 ** self.__inputSizes[i][2])
        return ans

    def isConnectedToInput(self):
        """
        @return bool : True if this block is connected to input, False otherwise.
        """
        return self.__isConnected

    @abstractmethod
    def isConnected(self):
        """
        @return bool : True if this block is connected to everything, False otherwise.
        """
        pass

    # left, right are for future versions. NOT USED IN CURRENT VERSION.
    def input(self, left=None, right=None):
        """
        @return obj : the instance of this class for connection purposes.
        """
        return self


class HasOutputConnections(Block):
    """
    A HasOutputConnections block is a block that has output connection wires.
    Examples include Machine, Combinational and Input.
    """

    def __init__(self, **kwargs):
        """
        Use keyword arguments to pass the following parameters:
        @param env : is the simpy environment.
        @param : blockID is the id of this input block. If blockID is duplicate or
                 None, then new unique ID is given.
        """
        maxOutSize = kwargs.get("maxOutSize", None)
        self.__maxOutSize = maxOutSize
        self.__state = (0, maxOutSize, maxOutSize)
        self.__fanOutList = []
        self._output = [0]
        self.__regList = []
        super().__init__(**kwargs)


    def addFanOut(self, other, val=0):
        if isinstance(other, HasRegisters) and val == 1:
            self.__regList.append(other)
        else:
            self.__fanOutList.append(other)


    def resetState(self):
        """
        Resets the state of the block.
        """
        self.__state = (0, self.__maxOutSize, self.__maxOutSize)

    def getLeft(self):
        """
        @return int : the left most bit of the output.
        """
        return self.__state[0]

    def getRight(self):
        """
        @return int : the right most bit of the output.
        """
        return self.__state[1]

    def getWidth(self):
        """
        @return int : the width of the output.
        """
        return self.__state[2]


    def __gt__(self, other):
        """
        Makes it possible to do the following connection:
        object1.output > object2.input
        """
        return other <= self

    def output(self, left=0, right=None):
        """
        @return obj : the instance of this class for connection purposes.
        """
        if (right == None):
            right = self.__maxOutSize
        self.__state = (left, right, right - left)
        return self

    def processFanOut(self):
        for i in self.__fanOutList:
            i.run()
        for i in self.__regList:
            i.runReg()

class HasOnlyOutputConnections(HasOutputConnections):
    """
    Class used by only those classes that only have output connections.
    These classes don't take any input.
    """

    def __init__(self, **kwargs):
        """
        Use keyword arguments to pass the following parameters:
        @param env : is the simpy environment.
        @param plot : is a boolean variable which represents whether or
                      not we should plot this class.
        @param blockID : is the id of this input block. If blockID is a
                         duplicate or None, then new unique ID is given.
        """
        super().__init__(**kwargs)

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


class HasRegisters(Block):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    ### we can change rising and falling edge

if __name__ == "__main__":

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
