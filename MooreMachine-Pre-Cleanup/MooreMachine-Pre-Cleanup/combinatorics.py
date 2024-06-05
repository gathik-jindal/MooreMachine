import simpy
from blocks import HasInputConnections, HasOutputConnections
from utilities import checkType


class Combinatorics(HasInputConnections, HasOutputConnections):
    """
    This class is used to create a combinatorial block.
    It requires a function to be passed to it which will be used to calculate the output.

    @param func: function that will be used to calculate the output.
    @param env: simpy.Environment object that will be used to run (timeout) the block.
    @param blockID: the unique ID of the block.
    @param plot: boolean that specifies whether the output of the block will be plotted or not.

    keyword arguments:
    @param state: the initial state of the block.
    """

    def __init__(self, func: function, env: simpy.Environment, blockID: str, delay: int = 0.1, plot: bool = False, **kwargs):
        
        checkType([(func, function), (env, simpy.Environment), (blockID, str), (delay, float), (plot, bool)])

        super().__init__(env, plot, blockID)
        self.__func = func
        self.__delay = delay
        self.__state = kwargs.get("state", 0)
        checkType([(self.__state, int)])


    def go(self):
        """
        Runs the block for the specified input and timeouts for the delay.
        """

        while True:
            yield self._output[self._connectedID].get()
            
            self.__state = self._input[0]
            self.state = self.__func(self.__state)
            
            if self.__plot:
                self._scopeDump.add(f"{self.blockID} input", self.env.now, self._input[0])
                
            yield self._env.timeout(self.__delay)
            self._output[0] = self.state

            if self.__plot:
                self._scopeDump.add(f"{self.blockID} output", self.env.now, self._output[0])

            for i in self._output:
                self._output[i].put(True)

    def run(self):

        self._env.process(self.go()) ##### check if __ or _
