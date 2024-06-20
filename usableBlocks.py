from blocks import *
from utilities import checkType, printErrorAndExit


class MooreMachine(HasInputConnections, HasOutputConnections, HasRegisters):
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
        @param : nsl_delay is the time taken by the NSL to run.
        @param : ol must be a valid function specifying output logic.
        @param : ol_delay is the time taken by the OL to run.
        @param : blockID is the id of this input block. If blockId is a duplicate
                 or None, then new unique ID is given.
        @param : register_delay is the time taken by the register to update.
        """
        self.nsl = kwargs.get("nsl")
        self.ol = kwargs.get("ol")
        self.nsl_delay = kwargs.get("nsl_delay", 0.01)
        self.ol_delay = kwargs.get("ol_delay", 0.01)
        super().__init__(**kwargs)
        self._scopeDump.add(f"Input to {self.getBlockID()}", 0, self._output[0])

    def __str__(self):
        """
        @return str : a string representation of this machine.
        """
        return f"MooreMachine ID {self.getBlockID()}"

    def __runNSL(self):
        """
        Runs the next state logic if the input to this machine changed.
        """
        # adding the inputs to scopedump
        self._scopeDump.add(f"Input to {self.getBlockID()}", self._env.now, self.getInputVal())

        # running the NSL
        tempout = self.nsl(self.getPS(), self.getInputVal())
        yield self._env.timeout(self.nsl_delay)

        # updating the next State
        self.setNS(tempout)
        self._scopeDump.add(f"NS of {self.getBlockID()}", self._env.now, self.getNS())

    def __runOL(self):
        """
        Output logic runs when the output value is changed.
        """

        temp = self.ol(self.getPS())
        yield self._env.timeout(self.ol_delay)
        self._output[0] = temp
        self._scopeDump.add(f"output of {self.getBlockID()}", self._env.now, self._output[0])

        # triggering events for the connected machines
        self.processFanOut()

    def runNSL(self):
        self._env.process(self.__runNSL())

    def runOL(self):
        self._env.process(self.__runOL())

    def run(self):
        """
        Runs this block.
        """
        self._env.process(self.__runNSL())
        self._env.process(self.__runOL())

    def isConnected(self):
        """
        @return bool : True if this block is connected to everything, False otherwise.
        """
        return self._clkVal != [] and self.nsl != None and self.ol != None and self.isConnectedToInput()

    # left, right are for future versions. NOT USED IN CURRENT VERSION.
    def input(self, left=None, right=None):
        """
        @return MooreMachine : the instance of this class for connection purposes.
        """
        self._isClock = 0  # 1 for clock, 0 for clock as input and -1 for not being used
        return self


class MealyMachine(HasInputConnections, HasOutputConnections, HasRegisters):
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
        @param : nsl_delay is the time taken by the NSL to run.
        @param : ol must be a valid function specifying output logic.
        @param : ol_delay is the time taken by the OL to run.
        @param : blockID is the id of this input block. If blockId is a duplicate
                 or None, then new unique ID is given.
        @param : register_delay is the time taken by the register to update.
        """
        self.nsl = kwargs.get("nsl")
        self.nsl_delay = kwargs.get("nsl_delay", 0.01)
        self.ol = kwargs.get("ol")
        self.ol_delay = kwargs.get("ol_delay", 0.01)
        super().__init__(**kwargs)
        self._scopeDump.add(f"Input to {self.getBlockID()}", 0, self._output[0])

    def __str__(self):
        """
        @return str : a string representation of this machine.
        """
        return f"Mealy Machine ID {self.getBlockID()}"

    def __runNSL(self):
        """
        Runs the next state logic if the input to this machine changed.
        """
        # adding the inputs to scopedump
        self._scopeDump.add(f"Input to {self.getBlockID()}", self._env.now, self.getInputVal())

        # running the NSL
        tempout = self.nsl(self.getPS(), self.getInputVal())
        yield self._env.timeout(self.nsl_delay)

        # updating the next State
        self.setNS(tempout)
        self._scopeDump.add(f"NS of {self.getBlockID()}", self._env.now, self.getNS())

    def __runOL(self):
        """
        Output logic runs when the output value is changed.
        """

        temp = self.ol(self.getPS(), self.getInputVal())
        yield self._env.timeout(self.ol_delay)
        self._output[0] = temp
        self._scopeDump.add(f"output of {self.getBlockID()}", self._env.now, self._output[0])

        # triggering events for the connected machines
        self.processFanOut()

    def runNSL(self):
        self._env.process(self.__runNSL())

    def runOL(self):
        self._env.process(self.__runOL())

    def run(self):
        """
        Runs this block.
        """
        self._env.process(self.__runNSL())
        self._env.process(self.__runOL())

    def isConnected(self):
        """
        @return bool : True if this block is connected to everything, False otherwise.
        """
        return self._clkVal != [] and self.nsl != None and self.ol != None and self.isConnectedToInput()

    # left, right are for future versions. NOT USED IN CURRENT VERSION.
    def input(self, left=None, right=None):
        """
        @return MooreMachine : the instance of this class for connection purposes.
        """
        self._isClock = 0  # 1 for clock, 0 for clock as input and -1 for not being used
        return self


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


class Register(Combinational, HasRegisters):
    """
    This class represents an 1 bit register.
    """

    def __init__(self, env, clock, delay: float, initialValue: int, plot: bool, blockID: str):
        """
        @param pydig : pydig object
        @param delay : the time delay for the register
        @param initialValue : The initial output value given by this block at t = 0 while running
        @param plot : boolean value whether to plot this block or not
        @param blockID : the id of this block. If None, then new unique ID is given.
        """
        checkType([(delay, (float, int)), (initialValue, int)])
        super().__init__(env=env, clk=clock, blockID=blockID, maxOutSize=1, delay=delay, plot=plot, initialValue=initialValue)

    def run(self):
        self.runReg()