"""
This file contains the implementation of the Synchronous Counter with Period.
The Synchronous Counter is a counter that increments its value only when
the clock signal is high.
The counter resets when the value of the counter reaches "period"
The counter is implemented using a Moore machine.
The Moore machine has the next state logic as the increment function and
the output logic as the identity function.
The counter is implemented using the Combinational block.

@author Abhirath, Aryan, Gathik
@date 4/5/2024
@version 1.6
"""

import os
import sys

# directory reach
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from utilities import checkType, printErrorAndExit, bitCount
from usableBlocks import Clock, Combinational as Comb
from pydig import pydig as pd

class SynchronousCounterWithPeriod(Comb):
    """
    This class contains the implementation of the Synchronous Counter with Period.
    The Synchronous Counter is a counter that increments its value only when
    the clock signal is high.
    The counter resets when the value of the counter reaches "period"
    The counter is implemented using a Moore machine.
    The Moore machine has the next state logic as the increment function and
    the output logic as the identity function.
    The counter is implemented using the Combinational block.
    """
    
    __counter = 0

    def __init__(self, pydig: pd, modValue: int, period: int, clock: Clock, plot: bool = True):
        """
        @param pydig : pydig object
        @param modValue : the maximum value of the counter
        @param period : the period of the counter
        @param clock : the clock signal
        @param plot : boolean value whether to plot this moore machine or not
        """
        checkType([(pydig, pd), (modValue, int), (clock, Clock), (plot, bool), (period, int)])
        maxOutSize = bitCount(modValue)
        self.__modValue = modValue
        SynchronousCounterWithPeriod.__counter += 1

        if (period >= modValue or period <= 0):
            printErrorAndExit(f"Period {period} must be between 1 and {modValue}")

        super().__init__(func=lambda x: x, env=pydig.getEnv(), blockID=f"Mod {modValue} Period {period} Counter {SynchronousCounterWithPeriod.__counter}", maxOutSize=maxOutSize, delay=0, plot=plot, state=0)

        o = pydig.combinationalFromObject(self)
        m = pydig.moore(plot=False, maxOutSize=maxOutSize, blockID=f"Moore {SynchronousCounterWithPeriod.__counter}")
        equal = pydig.combinational(maxOutSize=1, plot=False, blockID=f"Equality Comparator {SynchronousCounterWithPeriod.__counter}", func=lambda x: int(x == period), delay=0)
        self.__clk = clock

        m.nsl = self.__nsl
        m.ol = self.__ol

        equal.output() > m.input()
        self.__clk.output() > m.clock()
        m.output() > o.input()
        m.output() > equal.input()

    def __nsl(self, ps, i):
        """
        @param ps : the present state
        @param i : the input signal
        @return int : the next state
        """
        if (i == 1):
            return 0
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
    output1 = SynchronousCounterWithPeriod(pydig, 6, 4, clock, plot=True)

    pydig.generateCSV()
    pydig.run(until=30)
