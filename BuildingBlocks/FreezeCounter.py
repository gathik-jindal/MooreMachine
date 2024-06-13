"""
This file contains the class that is used to create a freeze counter.
A freeze counter is a type of counter in which if the input is high,
the counter "freezes" or, in other terms, stays at the same value until
the input becomes low again.

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

from pydig import pydig as pd
from usableBlocks import Clock as Clock, Combinational as Comb, HasOutputConnections as HOC
from utilities import checkType, bitCount


class FreezeCounter(Comb):
    """
    This class is used to create a freeze counter.
    When the input given is high, the counter value is frozen.
    """
    __counter = 0

    def __init__(self, pydig: pd, modValue: int, freeze: HOC, clock: Clock, plot: bool = True):
        """
        Creates a freeze counter object. 
        @param pydig : pydig object
        @param modValue : the maximum value of the counter
        @param freeze : the freeze signal
        @param clock : the clock signal
        @param plot : boolean value whether to plot this moore machine or not
        """
        checkType([(pydig, pd), (modValue, int), (freeze, HOC), (clock, Clock), (plot, bool)])
        maxOutSize = bitCount(modValue)
        self.__modValue = modValue
        FreezeCounter.__counter += 1

        super().__init__(func=lambda x: x, env=pydig.getEnv(), blockID=f"Mod {modValue} Freeze Counter {FreezeCounter.__counter}", maxOutSize=maxOutSize, delay=0, plot=plot, state=0)

        o = pydig.combinationalFromObject(self)
        i = freeze
        m = pydig.moore(plot=False, maxOutSize=maxOutSize, blockID=f"Moore {FreezeCounter.__counter}")
        self.__clk = clock

        m.nsl = self.__nsl
        m.ol = self.__ol

        i.output() > m.input()
        self.__clk.output() > m.clock()
        m.output() > o.input()

    def __nsl(self, ps, i):
        """
        @param ps : the present state
        @param i : the input signal
        @return int : the next state
        """
        if (i == 1):
            return ps
        return (ps + 1) % self.__modValue

    def __ol(self, ps):
        """
        @param ps : the present state
        @return int : the output signal
        """
        return ps

    def getScopeDump(self):
        """
        @return : the scope dump values for this block.
        """
        dic = self.__clk.getScopeDump()
        dic.update(self._scopeDump.getValues())
        return dic


if __name__ == "__main__":

    pydig = pd()
    clock = pydig.clock(blockID="", plot=False, timePeriod=1, onTime=0.5)
    i = pydig.source(filePath=".\\Tests\\FreezeCounter.csv", plot=False, blockID=f"Sync Reset")
    output1 = FreezeCounter(pydig, 6, i, clock, plot=True)

    pydig.generateCSV()
    pydig.run(until=30)
