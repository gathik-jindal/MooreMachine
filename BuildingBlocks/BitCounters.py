"""
This file contains 1 - 4 bit counters that take an enable line as input and 
the output is the actual output of the counter as well as the terminal count
of the counter. 
When the enable line is high, the counter starts counting and when the enable line
is low, the counter is frozen. 
The terminal count of the counter is high only when the counter's output is the max value
of the counter.

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
from blocks import Clock, Combinational as Comb, HasOutputConnections as HOC
from utilities import checkType


class Enabled1BitCounterWithTC(Comb):
    """
    This is an enabled 1 bit counter.
    The output of the counter is either 0 or 1. 
    When the output of the counter is 1, the terminal count of the counter is high.
    """

    __counter = 0

    def __init__(self, pydig: pd, syncReset: HOC, clock: Clock, plot: bool = True):
        """
        This creates an enabled 1 bit counter with terminal count object.
        @param pydig : a pydig object that you want to add this counter to.
        @param syncReset: a HasOutputConnection object (an Input object, a Machine object, or a Combinational object).
        @param clock : a clock object
        @param plot : a boolean value whether to plot this object or not
        """

        checkType([(pydig, pd), (syncReset, HOC),
                  (clock, Clock), (plot, bool)])

        Enabled1BitCounterWithTC.__counter += 1

        super().__init__(func=lambda x: x & 1, env=pydig.getEnv(), blockID=f"Enabled 1 Bit Counter {Enabled1BitCounterWithTC.__counter}", maxOutSize=1, delay=0, plot=plot, state=0)

        o = pydig.combinationalFromObject(self)
        self.__tc = pydig.combinational(maxOutSize=1, plot=False, blockID=f"Enabled 1 Bit Counter TC {Enabled1BitCounterWithTC.__counter}",func=lambda x: (x & 2) >> 1)
        i = syncReset
        m = pydig.moore(plot=False, maxOutSize=2, blockID=f"Moore {Enabled1BitCounterWithTC.__counter}")
        self.__clk = clock

        m.nsl = self.__nsl
        m.ol = self.__ol

        i.output() > m.input()
        self.__clk.output() > m.clock()
        m.output() > o.input()
        m.output() > self.__tc.input()

    def __nsl(self, ps, i):
        """
        Computes the next state logic for this counter.
        @param ps : the present state
        @param i : the input (enable)
        @return int : the next state of the counter
        """

        return ps ^ i

    def __ol(self, ps):
        """
        Computes the output logic for this counter.
        @param ps : the present state
        @return int : the output of the counter : 1st bit is TC, the second bit is the output
        """

        return ps << 1 | ps

    def getTerminalCount(self):
        """
        Returns the terminal count object.
        @return Combinational : The terminal count
        """

        return self.__tc
    
    def getScopeDump(self):
        """
        @return : the scope dump values for this block.
        """
        dic = self.__clk.getScopeDump()
        dic.update(self._scopeDump.getValues())
        return dic


class Enabled2BitCounterWithTC(Comb):
    """
    This is an enabled 2 bit counter.
    The output of the counter is either 0 - 3. 
    When the output of the counter is 3, the terminal count of the counter is high.
    """

    __counter = 0

    def __init__(self, pydig: pd, syncReset: HOC, clock: Clock, plot: bool = True):
        """
        This creates an enabled 2 bit counter with terminal count object.
        @param pydig : a pydig object that you want to add this counter to.
        @param syncReset: a HasOutputConnection object (an Input object, a Machine object, or a Combinational object).
        @param clock : a clock object
        @param plot : a boolean value whether to plot this object or not
        """

        checkType([(pydig, pd), (syncReset, HOC), (clock, Clock), (plot, bool)])

        Enabled2BitCounterWithTC.__counter += 1

        self.__c1 = Enabled1BitCounterWithTC(
            pydig, syncReset, clock, plot=False)

        temp = pydig.combinational(maxOutSize=1, plot=False, blockID=f"Enabled 2 Bit Counter And{Enabled2BitCounterWithTC.__counter}", func=lambda x: (x >> 1 & 1) & (x & 1))

        self.__c2 = Enabled1BitCounterWithTC(
            pydig, temp.output(), clock, plot=False)

        Comb.__init__(self, func=lambda x: x, env=pydig.getEnv(), blockID=f"Enabled 2 Bit Counter {Enabled2BitCounterWithTC.__counter}", maxOutSize=2, delay=0, plot=plot, state=0)
        o = pydig.combinationalFromObject(self)
        self.__tc = pydig.combinational(maxOutSize=1, plot=False, blockID=f"Enabled 2 Bit Counter TC{Enabled2BitCounterWithTC.__counter}", func=lambda x: (x >> 1 & 1) & (x & 1))

        self.__clk = clock

        self.__c1.output() > o.input()
        self.__c2.output() > o.input()
        syncReset.output() > temp.input()
        self.__c1.getTerminalCount().output() > temp.input()
        self.__c1.getTerminalCount().output() > self.__tc.input()
        self.__c2.getTerminalCount().output() > self.__tc.input()

    def getTerminalCount(self):
        """
        Returns the terminal count object.
        @return Combinational : The terminal count
        """

        return self.__tc
    
    def getScopeDump(self):
        """
        @return : the scope dump values for this block.
        """
        dic = self.__clk.getScopeDump()
        dic.update(self._scopeDump.getValues())
        return dic


class Enabled3BitCounterWithTC(Comb):
    """
    This is an enabled 3 bit counter.
    The output of the counter is either 0 - 7. 
    When the output of the counter is 7, the terminal count of the counter is high.
    """

    __counter = 0

    def __init__(self, pydig: pd, syncReset: HOC, clock: Clock, plot: bool = True):
        """
        This creates an enabled 3 bit counter with terminal count object.
        @param pydig : a pydig object that you want to add this counter to.
        @param syncReset: a HasOutputConnection object (an Input object, a Machine object, or a Combinational object).
        @param clock : a clock object
        @param plot : a boolean value whether to plot this object or not
        """

        checkType([(pydig, pd), (syncReset, HOC), (clock, Clock), (plot, bool)])

        Enabled3BitCounterWithTC.__counter += 1

        self.__c1 = Enabled1BitCounterWithTC(
            pydig, syncReset, clock, plot=False)

        temp = pydig.combinational(maxOutSize=1, plot=False, blockID=f"Enabled 3 Bit Counter And{Enabled3BitCounterWithTC.__counter}", func=lambda x: (x >> 1 & 1) & (x & 1))

        self.__c2 = Enabled2BitCounterWithTC(
            pydig, temp.output(), clock, plot=False)

        Comb.__init__(self, func=lambda x: x, env=pydig.getEnv(), blockID=f"Enabled 3 Bit Counter {Enabled3BitCounterWithTC.__counter}", maxOutSize=3, delay=0, plot=plot, state=0)
        o = pydig.combinationalFromObject(self)
        self.__tc = pydig.combinational(maxOutSize=1, plot=False, blockID=f"Enabled 3 Bit Counter TC{Enabled3BitCounterWithTC.__counter}", func=lambda x: (x >> 1 & 1) & (x & 1))

        self.__clk = clock

        self.__c1.output() > o.input()
        self.__c2.output() > o.input()
        syncReset.output() > temp.input()
        self.__c1.getTerminalCount().output() > temp.input()
        self.__c1.getTerminalCount().output() > self.__tc.input()
        self.__c2.getTerminalCount().output() > self.__tc.input()

    def getTerminalCount(self):
        """
        Returns the terminal count object.
        @return Combinational : The terminal count
        """

        return self.__tc

    def getScopeDump(self):
        """
        @return : the scope dump values for this block.
        """
        dic = self.__clk.getScopeDump()
        dic.update(self._scopeDump.getValues())
        return dic


class Enabled4BitCounterWithTC(Comb):
    """
    This is an enabled 4 bit counter.
    The output of the counter is either 0 - 15. 
    When the output of the counter is 15, the terminal count of the counter is high.
    """

    __counter = 0

    def __init__(self, pydig: pd, syncReset: HOC, clock: Clock, plot: bool = True):
        """
        This creates an enabled 4 bit counter with terminal count object.
        @param pydig : a pydig object that you want to add this counter to.
        @param syncReset: a HasOutputConnection object (an Input object, a Machine object, or a Combinational object).
        @param clock : a clock object
        @param plot : a boolean value whether to plot this object or not
        """

        checkType([(pydig, pd), (syncReset, HOC), (clock, Clock), (plot, bool)])

        Enabled4BitCounterWithTC.__counter += 1

        self.__c1 = Enabled2BitCounterWithTC( pydig, syncReset, clock, plot=False)

        temp = pydig.combinational(maxOutSize=1, plot=False, blockID=f"Enabled 4 Bit Counter And{Enabled4BitCounterWithTC.__counter}", func=lambda x: (x >> 1 & 1) & (x & 1))

        self.__c2 = Enabled2BitCounterWithTC( pydig, temp.output(), clock, plot=False)

        Comb.__init__(self, func=lambda x: x, env=pydig.getEnv(), blockID=f"Enabled 4 Bit Counter {Enabled4BitCounterWithTC.__counter}", maxOutSize=4, delay=0, plot=plot, state=0)
        o = pydig.combinationalFromObject(self)
        self.__tc = pydig.combinational(maxOutSize=1, plot=False, blockID=f"Enabled 4 Bit Counter TC{Enabled4BitCounterWithTC.__counter}", func=lambda x: (x >> 1 & 1) & (x & 1))

        self.__clk = clock

        self.__c1.output() > o.input()
        self.__c2.output() > o.input()
        syncReset.output() > temp.input()
        self.__c1.getTerminalCount().output() > temp.input()
        self.__c1.getTerminalCount().output() > self.__tc.input()
        self.__c2.getTerminalCount().output() > self.__tc.input()

    def getTerminalCount(self):
        """
        Returns the terminal count object.
        @return Combinational : The terminal count
        """

        return self.__tc

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
    input1 = pydig.source(filePath="Tests\\BitCounter.csv", plot=False, blockID="Input")
    output1 = Enabled4BitCounterWithTC(pydig, input1, clock, plot=True)

    pydig.generateCSV()
    pydig.run(until=60)
