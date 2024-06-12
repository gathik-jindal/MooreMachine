from blocks import *
from utilities import checkType, printErrorAndExit


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
        self.__clkVal = kwargs.get("clk", [])  # make it always []
        self.__clkObj = None
        self.__isClock = 0
        startingState = kwargs.get("startingState", 0)
        self.__presentState = startingState
        self.__nextState = startingState
        super().__init__(**kwargs)
        self._scopeDump.add(f"Input to {self.getBlockID()}", 0, self._output[0])

    def __str__(self):
        """
        @return str : a string representation of this machine.
        """
        return f"Machine ID {self.getBlockID()}"

    def __runNSL(self):
        """
        Runs the next state logic if the input to this machine changed.
        """
        # adding the inputs to scopedump
        self._scopeDump.add(f"Input to {self.getBlockID()}", self._env.now, self.getInputVal())

        # running the NSL
        tempout = self.nsl(self.__presentState, self.getInputVal())
        yield self._env.timeout(timeout)

        # updating the next State
        self.__nextState = tempout
        self._scopeDump.add(f"NS of {self.getBlockID()}", self._env.now, self.__nextState)

    def __runReg(self):
        """
        Registers run based on clock.
        """
        if (self.__clkVal[0]):
            if self.__presentState != self.__nextState:
                yield self._env.timeout(timeout)
                self.__presentState = self.__nextState
                self._scopeDump.add(f"PS of {self.getBlockID()}", self._env.now, self.__presentState)
                self._env.process(self.__runOL())
                self._env.process(self.__runNSL())

    def __runOL(self):
        """
        Output logic runs when the output value is changed.
        """

        temp = self.ol(self.__presentState)
        yield self._env.timeout(timeout)
        self._output[0] = temp
        self._scopeDump.add(f"output of {self.getBlockID()}", self._env.now, self._output[0])

        # triggering events for the connected machines
        self.processFanOut()

    def runReg(self):
        self._env.process(self.__runReg())

    def run(self):
        """
        Runs this block.
        """
        self._env.process(self.__runNSL())
        if self._env.now == 0:
            self._env.process(self.__runOL())

    def isConnected(self):
        """
        @return bool : True if this block is connected to everything, False otherwise.
        """
        return self.__clkVal != [] and self.nsl != None and self.ol != None and self.isConnectedToInput()

    def clock(self):
        """
        Connects the next clock object to the Register
        @return Machine : the instance of this class for connection purposes.
        """
        self.__isClock = 1  # 1 for clock, 0 for clock as input and -1 for not being used
        return self

    # left, right are for future versions. NOT USED IN CURRENT VERSION.
    def input(self, left=None, right=None):
        """
        @return Machine : the instance of this class for connection purposes.
        """
        self.__isClock = 0  # 1 for clock, 0 for clock as input and -1 for not being used
        return self

    def getScopeDump(self):
        """
        @return dict : the scope dump values for this block.
        """
        dic = self.__clkObj.getScopeDump()
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
        if (self.__isClock == 1):
            self.__clkVal = other._output
            other.addFanOut(self, 1)
            self.__clkObj = other
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

        self.__input = inputList
        super().__init__(maxOutSize=maxOutSize, **kwargs)
        self._scopeDump.add(f"Input to {self.getBlockID()}", 0, self._output[0])

    def __str__(self):
        """
        @return str : the string representation of this input block.
        """
        return f"Input ID {self.getBlockID()}"

    def _go(self):
        """
        Runs the input at every change in input value specified by inputList.
        """
        for i in self.__input:
            yield self._env.timeout(i[0]-self._env.now)

            self._output[0] = i[1]
            self._scopeDump.add(f"Input to {self.getBlockID()}", self._env.now, self._output[0])
            self.processFanOut()


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
        timePeriod = kwargs.get("timePeriod", 1)
        onTime = kwargs.get("onTime", 0.5)
        initialValue = kwargs.get("initialValue", 0)

        checkType([(timePeriod, (int, float)),(onTime, (int, float)), (initialValue, int)])
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
        return f"Clock ID {self.getBlockID()}"

    def _go(self):
        """
        Runs the clock at every time period.
        """
        while True:
            yield self._env.timeout((1-self._output[0])*(self.__timePeriod - self.__onTime)+self._output[0]*(self.__onTime))
            self._output[0] = 1 - self._output[0]
            self._scopeDump.add(f"Clock {self.getBlockID()}", self._env.now, self._output[0])
            self.processFanOut()


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
        return f"Output ID {self.getBlockID()}"

    def __give(self):
        """
        Adds the output value to this class every time there is a change in it.
        """
        yield self._env.timeout(0.01)
        self._scopeDump.add(f"Final Output from {self.getBlockID()}", self._env.now, self.getInputVal())

    def run(self):
        """
        Runs the output block
        """
        self._env.process(self.__give())

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
        self._scopeDump.add(f"{self.getBlockID()} output", 0, self._output[0])

    def __runFunc(self):
        """
        Runs the block for the specified input and timeouts for the delay.
        """

        self.__value = self.getInputVal()
        self.__value = self.__func(self.__value)

        yield self._env.timeout(self.__delay)
        self._output[0] = self.__value

        self._scopeDump.add(f"{self.getBlockID()} output", self._env.now, self._output[0])

        self.processFanOut()

    def __str__(self):
        """
        @return str : a string representation of the block.
        """
        return f"Combinational ID {self.getBlockID()}"

    def run(self):
        """
        Runs this block.
        """
        self._env.process(self.__runFunc())

    def isConnected(self):
        """
        @return bool : True if this block is connected to everything, False otherwise.
        """
        return self.isConnectedToInput()
