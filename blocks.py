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
        self._blockID = kwargs.get("blockID", 0)

    def getBlockID(self):
        """
        Returns the block ID of the current block.
        @return str : blockID
        """
        return self._blockID

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
        self._trigger = simpy.Store(kwargs.get("env", None))
        self._input = []
        self._inputSizes = []
        self._inputCount = 0
        self._isConnected = False
        self._connectedID = []
        self._clockID = None
        super().__init__(**kwargs)

    def __le__(self, other):
        """
        The output of other goes into the input of self.
        If the inputs of self are already connected, then error is generated.

        @param other : must be of type HasOutputConnections.
        @return bool : True
        """

        checkType([(other, (HasOutputConnections))])
        self._input.append(other._output)
        self._inputSizes.append((other.getLeft(), other.getRight(), other.getWidth()))
        self._inputCount += 1
        self._connectedID.append(other.addFanout())
        self._isConnected = True
        other.resetState()
        return True

    def getInputCount(self):
        """
        @return int: the number of inputs connected to this block.
        """
        return self._inputCount

    def _strip(self, val, left, right):
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
        for i in range(self._inputCount):
            ans += self._strip(self._input[i][0], self._inputSizes[i][0], self._inputSizes[i][1]) * factor
            factor = factor * (2 ** self._inputSizes[i][2])
        return ans

    def isConnectedToInput(self):
        """
        @return bool : True if this block is connected to input, False otherwise.
        """
        return self._isConnected

    @abstractmethod
    def isConnected(self):
        """
        @return bool : True if this block is connected to everything, False otherwise.
        """
        pass

    def runTriggers(self):
        """
        Readys all the triggering processes.
        """
        for i in range(self.getInputCount()):
            self._env.process(self.__runTriggers(self._trigger, self._input[i][self._connectedID[i]]))

    def __runTriggers(self, triggerObj, checkObj):
        """
        A private method that runs the triggers for the connected blocks.
        @param triggerObj : simpy.Store() object waiting to be triggered
        @param checkObj : simpy.Store() object to be checked for triggering
        """
        while True:
            yield checkObj.get()
            if (len(triggerObj.items) < 1):
                triggerObj.put(True)

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
        self.defineFanOut()
        super().__init__(**kwargs)

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
        @return int : the number of output components connected to this block.
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

    def output(self, left=0, right=None):
        """
        @return obj : the instance of this class for connection purposes.
        """
        if (right == None):
            right = self.__maxOutSize
        self.__state = (left, right, right - left)
        return self


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


class Machine(HasInputConnections, HasOutputConnections):
    """
    A machine is both a HasInputConnections block and a HasOutputConnections block.
    This represents the Moore Machine.
    """

    def __init__(self, **kwargs):
        """
        Use keyword arguments to pass the following parameters:
        @param : env must be a simpy environment.
        @param : clock must be of type Clock.
        @param : nsl must be a valid function specifying next state logic.
        @param : ol must be a valid function specifying output logic.
        @param : blockID is the id of this input block. If blockId is a duplicate
                 or None, then new unique ID is given.
        """
        self.nsl = kwargs.get("nsl")
        self.ol = kwargs.get("ol")
        self.clk = kwargs.get("clk", None)
        startingState = kwargs.get("startingState", 0)
        self.presentState = startingState
        self.nextState = startingState
        self._Pchange = simpy.Store(kwargs.get("env", None))
        self._Pchange.put(False)
        super().__init__(**kwargs)
        self._scopeDump.add(f"Input to {self.getBlockID()}", 0, self._output[0])

    def __str__(self):
        """
        @return str : a string representation of this machine.
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
            yield self._env.timeout(timeout)

            # updating the next State
            self.nextState = tempout
            self._scopeDump.add(f"NS of {self.getBlockID()}", self._env.now, self.nextState)


    def __runNSLp(self):
        """
        Runs the next state logic if the present state changed. 
        """

        while True:
            yield self._Pchange.get()

            # running the NSL
            tempout = self.nsl(self.presentState, self.getInputVal())
            yield self._env.timeout(timeout)

            # updating the output
            self.nextState = tempout
            self._scopeDump.add(f"NS of {self.getBlockID()}", self._env.now, self.nextState)

    def __runReg(self):
        """
        Registers run based on clock.
        """

        while True:
            output = yield self.clk[self._clockID].get()
            if (output):
                if self.presentState == self.nextState:
                    continue
                yield self._env.timeout(timeout)
                self.presentState = self.nextState
                self._scopeDump.add(f"PS of {self.getBlockID()}", self._env.now, self.presentState)
                self._Pchange.put(True)
                self._env.process(self.__runOL())

    def __runOL(self):
        """
        Output logic runs when the output value is changed.
        """

        temp = self.ol(self.presentState)
        yield self._env.timeout(timeout)
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
        """
        @return bool : True if this block is connected to everything, False otherwise.
        """
        return self.clk != None and self.nsl != None and self.ol != None and self.isConnectedToInput()

    def clock(self):
        """
        Connects the next clock object to the Register
        @return Machine : the instance of this class for connection purposes.
        """
        self._isClock = 1  # 1 for clock, 0 for clock as input and -1 for not being used
        return self

    # left, right are for future versions. NOT USED IN CURRENT VERSION.
    def input(self, left=None, right=None):
        """
        @return Machine : the instance of this class for connection purposes.
        """
        self._isClock = 0  # 1 for clock, 0 for clock as input and -1 for not being used
        return self

    def getScopeDump(self):
        """
        @return dict : the scope dump values for this block.
        """
        dic = self._clkObj.getScopeDump()
        dic.update(self._scopeDump.getValues())
        return dic

    def __le__(self, other):
        """
        The output of other goes into the input of self.
        If the inputs of self are already connected, then error is generated.

        @param other : must be of type HasOutputConnections.
        @return : bool
        """
        # state 1 means clock, 0 means clock (but as input)
        if (isinstance(other, Clock) and self._isClock == 1):
            self.clk = other._output
            self._clockID = other.addFanout()
            self._clkObj = other
            return True
        else:
            return super().__le__(other)


class Input(HasOnlyOutputConnections):
    """
    An input is a HasOutputConnections block.
    This takes the input values from a file and passes it on in a format understood by the simulator.
    """

    def __init__(self, **kwargs):
        """
        Use keyword arguments to pass the following parameters:
        @param inputList : must be a list that contains the input changes
                           at the time intervals.
        @param env : is the simpy environment.
        @param blockID : is the id of this input block. If blockID is a
                         duplicate or None, then new unique ID is given.
        """
        inputList = kwargs.get("inputList", [(0, 0)])

        maxOutSize = 2
        for i in inputList:
            if (len(bin(i[1])) > maxOutSize):
                maxOutSize = len(bin(i[1]))
        maxOutSize -= 2

        self._input = inputList
        super().__init__(maxOutSize=maxOutSize, **kwargs)
        self._scopeDump.add(f"Input to {self.getBlockID()}", 0, self._output[0])

    def __str__(self):
        """
        @return str : the string representation of this input block.
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

            self._scopeDump.add(f"Input to {self.getBlockID()}", self._env.now, self._output[0])


class Clock(HasOnlyOutputConnections):
    """
    A clock is a HasOutputConnections block.
    This represents the Clock Block.
    """

    def __init__(self, **kwargs):
        """
        Use keyword arguments to pass the following parameters:
        @param timePeriod : the time period of the clock.
        @param onTime : the amount of time in each cycle that the clock shows high.
        @param env : is the simpy environment.
        @param blockID : is the id of this input block. If blockID is a
                         duplicate or None, then new unique ID is given.
        @param initialValue : is the initial state of the clock.
        """
        timePeriod = kwargs.get("timePeriod", 1.2)
        onTime = kwargs.get("onTime", 0.6)
        initialValue = kwargs.get("initialValue", 0)

        checkType([(timePeriod, (int, float)), (onTime, (int, float)), (initialValue, int)])
        if (timePeriod < onTime):
            printErrorAndExit(f"Clock {self} cannot have timePeriod = {timePeriod} less than onTime = {onTime}.")

        self.__timePeriod = timePeriod
        self.__onTime = onTime

        super().__init__(**kwargs)
        self._output[0] = initialValue
        self._scopeDump.add(f"Clock {self.getBlockID()}", 0, self._output[0])

    # left, right are for future versions. NOT USED IN CURRENT VERSION.
    def output(self, left=None, right=None):
        """
        @return Clock : this object for connection purposes.
        """
        return self

    def __str__(self):
        """
        @return str : the string representation of this clock block.
        """
        return f"Clock ID {self._blockID}"

    def _go(self):
        """
        Runs the clock at every time period.
        """
        
        while True:
            yield self._env.timeout((1-self._output[0])*(self.__timePeriod - self.__onTime)+self._output[0]*(self.__onTime))

            self._output[0] = 1 - self._output[0]

            for i in range(1, self._fanOutCount+1):
                self._output[i].put(self._output[0])

            self._scopeDump.add(f"Clock {self.getBlockID()}", self._env.now, self._output[0])


class Output(HasInputConnections):
    """
    An Output is a HasInputConnections block.
    This represents the Output Block.
    blockID is the id of this input block. If None, 
    then new unique ID is given.
    """

    def __init__(self, **kwargs):
        """
        Use keyword arguments to pass the following parameters:
        @param env : is a simpy environment.
        @param blockID : is the id of this input block. If blockID is a
                            duplicate or None, then new unique ID is given.
        """
        super().__init__(**kwargs)

    def __str__(self):
        """
        @return str : a string representation of the output block.
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
        """
        @return bool : True if this block is connected to everything, False otherwise.
        """
        return self.isConnectedToInput()


class Combinational(HasInputConnections, HasOutputConnections):
    """
    This class is used to create a combinatorial block.
    It requires a function to be passed to it which will be used to calculate the output.
    """

    def __init__(self, **kwargs):
        """
        Use keyword arguments to pass the following parameters:
        @param func : is the function that will be used to calculate the output.
        @param delay : is the delay in the output.
        @param env : is the simpy environment.
        @param plot : is a boolean variable which represents whether or not we should plot this class.
        @param blockID : is the id of this input block. If blockID is a duplicate or None, then new unique ID is given.
        @param initialValue : the initial value of the block.
        """
        func = kwargs.get("func", None)
        delay = kwargs.get("delay", 0)
        initialValue = kwargs.get("initialValue", 0)
        checkType([(initialValue, int), (delay, (float, int))])
        self.__func = func
        self.__delay = delay
        self.__value = initialValue
        super().__init__(**kwargs)
        self._output[0] = initialValue
        self._scopeDump.add(f"{self._blockID} output", 0, self._output[0])
        
    def go(self):
        """
        Runs the block for the specified input and timeouts for the delay.
        """
        while True:
            yield self._trigger.get()

            self.__value = self.getInputVal()
            self.__value = self.__func(self.__value)

            yield self._env.timeout(self.__delay)
            self._output[0] = self.__value

            self._scopeDump.add(f"{self._blockID} output", self._env.now, self._output[0])

            for i in range(1, self._fanOutCount+1):
                self._output[i].put(True)

    def __str__(self):
        """
        @return str : a string representation of the block.
        """
        return f"Combinational ID {self._blockID}"

    def run(self):
        """
        Runs this block.
        """
        self._env.process(self.go())
        self.runTriggers()

    def isConnected(self):
        """
        @return bool : True if this block is connected to everything, False otherwise.
        """
        return self.isConnectedToInput()


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
